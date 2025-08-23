import re
import uuid
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import Visitor, PageView, DailyStats
from django.db import transaction
from datetime import date


class VisitorTrackingMiddleware(MiddlewareMixin):
    """
    Middleware لتتبع زوار الموقع تلقائياً
    """
    
    def get_client_ip(self, request):
        """الحصول على عنوان IP الحقيقي للزائر"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_device_type(self, user_agent):
        """تحديد نوع الجهاز من User Agent"""
        if not user_agent:
            return 'unknown'
        
        user_agent = user_agent.lower()
        
        # تحديد الجوالات
        mobile_patterns = [
            r'mobile', r'android', r'iphone', r'ipod', 
            r'blackberry', r'windows phone', r'opera mini'
        ]
        
        # تحديد التابلت
        tablet_patterns = [
            r'tablet', r'ipad', r'android(?!.*mobile)', 
            r'kindle', r'silk'
        ]
        
        for pattern in mobile_patterns:
            if re.search(pattern, user_agent):
                return 'mobile'
        
        for pattern in tablet_patterns:
            if re.search(pattern, user_agent):
                return 'tablet'
        
        return 'desktop'
    
    def process_request(self, request):
        """معالجة الطلب وتسجيل بيانات الزائر"""
        # تجاهل طلبات الملفات الثابتة والإدارة
        if (request.path.startswith('/static/') or 
            request.path.startswith('/media/') or
            request.path.startswith('/admin/') or
            request.path.startswith('/favicon.ico')):
            return None
        
        try:
            # الحصول على معرف الزائر من الكوكيز أو إنشاء جديد
            visitor_id = request.COOKIES.get('visitor_id')
            if not visitor_id:
                visitor_id = str(uuid.uuid4())
            
            # الحصول على بيانات الطلب
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            referrer = request.META.get('HTTP_REFERER')
            page_url = request.path
            device_type = self.get_device_type(user_agent)
            
            # البحث عن الزائر أو إنشاء جديد
            with transaction.atomic():
                visitor, created = Visitor.objects.get_or_create(
                    visitor_id=visitor_id,
                    defaults={
                        'ip_address': ip_address,
                        'user_agent': user_agent,
                        'page_visited': page_url,
                        'referrer': referrer,
                        'device_type': device_type,
                        'visit_count': 1
                    }
                )
                
                # إذا كان الزائر موجود، نحديث بياناته
                if not created:
                    visitor.visit_count += 1
                    visitor.last_visit = timezone.now()
                    visitor.page_visited = page_url
                    if not visitor.user_agent:
                        visitor.user_agent = user_agent
                    visitor.save()
                
                # تسجيل مشاهدة الصفحة
                PageView.objects.create(
                    visitor=visitor,
                    page_url=page_url,
                    page_title=self.get_page_title(page_url)
                )
                
                # تحديث الإحصائيات اليومية
                self.update_daily_stats()
            
            # حفظ معرف الزائر في الطلب للاستخدام لاحقاً
            request.visitor_id = visitor_id
            request.visitor = visitor
            
        except Exception as e:
            # في حالة حدوث خطأ، نسجله ونتجاهله لعدم تعطيل الموقع
            print(f"Error in visitor tracking: {e}")
        
        return None
    
    def process_response(self, request, response):
        """معالجة الاستجابة وتعيين الكوكيز"""
        if hasattr(request, 'visitor_id'):
            # تعيين كوكيز معرف الزائر لمدة 30 يوم
            response.set_cookie(
                'visitor_id', 
                request.visitor_id, 
                max_age=30*24*60*60,  # 30 يوم
                httponly=True,
                samesite='Lax'
            )
        return response
    
    def get_page_title(self, page_url):
        """الحصول على عنوان الصفحة"""
        page_titles = {
            '/': 'الصفحة الرئيسية - الدكتور أحمد أبو صفية',
            '/services/': 'الخدمات',
            '/contact/': 'تواصل معنا',
        }
        return page_titles.get(page_url, 'صفحة غير معروفة')
    
    def update_daily_stats(self):
        """تحديث الإحصائيات اليومية"""
        try:
            today = date.today()
            
            # حساب الإحصائيات
            unique_visitors_today = Visitor.objects.filter(
                first_visit__date=today
            ).count()
            
            total_page_views_today = PageView.objects.filter(
                timestamp__date=today
            ).count()
            
            # تحديث أو إنشاء سجل الإحصائيات اليومية
            daily_stats, created = DailyStats.objects.get_or_create(
                date=today,
                defaults={
                    'unique_visitors': unique_visitors_today,
                    'total_page_views': total_page_views_today,
                }
            )
            
            if not created:
                daily_stats.unique_visitors = unique_visitors_today
                daily_stats.total_page_views = total_page_views_today
                daily_stats.save()
                
        except Exception as e:
            print(f"Error updating daily stats: {e}")


class ClickTrackingMixin:
    """
    Mixin لتتبع النقرات على الأزرار المهمة
    يمكن استخدامه في JavaScript لإرسال بيانات النقرات
    """
    pass
