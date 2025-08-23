from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Visitor, PageView, ClickEvent, DailyStats, ContactMessage
import json


class VisitorAdmin(admin.ModelAdmin):
    """
    واجهة إدارة الزوار
    """
    list_display = [
        'ip_address', 'device_type', 'visit_count', 
        'is_engaged', 'country', 'first_visit', 'last_visit'
    ]
    list_filter = [
        'device_type', 'is_engaged', 'country', 
        'first_visit', 'last_visit'
    ]
    search_fields = ['ip_address', 'country', 'city']
    readonly_fields = ['visitor_id', 'first_visit', 'last_visit']
    list_per_page = 50
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('visitor_id', 'ip_address', 'device_type')
        }),
        ('معلومات الموقع', {
            'fields': ('country', 'city', 'page_visited')
        }),
        ('إحصائيات الزيارة', {
            'fields': ('visit_count', 'session_duration', 'is_engaged')
        }),
        ('معلومات تقنية', {
            'fields': ('user_agent', 'referrer'),
            'classes': ('collapse',)
        }),
        ('التواريخ', {
            'fields': ('first_visit', 'last_visit')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


class PageViewAdmin(admin.ModelAdmin):
    """
    واجهة إدارة مشاهدات الصفحات
    """
    list_display = ['page_url', 'visitor_ip', 'timestamp', 'time_spent']
    list_filter = ['timestamp', 'page_url']
    search_fields = ['page_url', 'visitor__ip_address']
    readonly_fields = ['timestamp']
    list_per_page = 100
    
    def visitor_ip(self, obj):
        return obj.visitor.ip_address
    visitor_ip.short_description = 'عنوان IP'


class ClickEventAdmin(admin.ModelAdmin):
    """
    واجهة إدارة النقرات
    """
    list_display = ['element_clicked', 'visitor_ip', 'page_url', 'timestamp']
    list_filter = ['element_clicked', 'timestamp', 'page_url']
    search_fields = ['visitor__ip_address', 'page_url']
    readonly_fields = ['timestamp']
    list_per_page = 100
    
    def visitor_ip(self, obj):
        return obj.visitor.ip_address
    visitor_ip.short_description = 'عنوان IP'


class DailyStatsAdmin(admin.ModelAdmin):
    """
    واجهة إدارة الإحصائيات اليومية
    """
    list_display = [
        'date', 'unique_visitors', 'total_page_views', 
        'total_clicks', 'avg_session_duration', 'conversion_rate'
    ]
    list_filter = ['date']
    readonly_fields = ['date']
    list_per_page = 31


class ContactMessageAdmin(admin.ModelAdmin):
    """
    واجهة إدارة رسائل التواصل
    """
    list_display = ['name', 'email', 'service', 'created_at', 'is_read']
    list_filter = ['service', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']
    list_per_page = 50
    
    fieldsets = (
        ('معلومات المرسل', {
            'fields': ('name', 'email', 'phone')
        }),
        ('تفاصيل الرسالة', {
            'fields': ('service', 'message')
        }),
        ('إدارة', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} رسالة تم تعليمها كمقروءة.')
    mark_as_read.short_description = 'تعليم كمقروءة'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} رسالة تم تعليمها كغير مقروءة.')
    mark_as_unread.short_description = 'تعليم كغير مقروءة'


class CustomAdminSite(admin.AdminSite):
    """
    موقع إدارة مخصص مع لوحة إحصائيات
    """
    site_header = 'إدارة موقع الدكتور أحمد أبو صفية'
    site_title = 'إدارة الموقع'
    index_title = 'لوحة التحكم والإحصائيات'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.statistics_view, name='statistics'),
        ]
        return custom_urls + urls
    
    def statistics_view(self, request):
        """
        عرض صفحة الإحصائيات المفصلة
        """
        # إحصائيات عامة
        total_visitors = Visitor.objects.count()
        total_page_views = PageView.objects.count()
        total_clicks = ClickEvent.objects.count()
        
        # إحصائيات اليوم
        today = timezone.now().date()
        today_visitors = Visitor.objects.filter(first_visit__date=today).count()
        today_page_views = PageView.objects.filter(timestamp__date=today).count()
        today_clicks = ClickEvent.objects.filter(timestamp__date=today).count()
        
        # إحصائيات آخر 7 أيام
        last_7_days = timezone.now() - timedelta(days=7)
        weekly_visitors = Visitor.objects.filter(first_visit__gte=last_7_days).count()
        
        # إحصائيات آخر 30 يوم
        last_30_days = timezone.now() - timedelta(days=30)
        monthly_visitors = Visitor.objects.filter(first_visit__gte=last_30_days).count()
        
        # إحصائيات الأجهزة
        device_stats = Visitor.objects.values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # أكثر الصفحات زيارة
        popular_pages = PageView.objects.values('page_url').annotate(
            views=Count('id')
        ).order_by('-views')[:10]
        
        # أكثر الأزرار نقراً
        popular_buttons = ClickEvent.objects.values('element_clicked').annotate(
            clicks=Count('id')
        ).order_by('-clicks')[:10]
        
        # إحصائيات يومية لآخر 30 يوم (للرسم البياني)
        daily_stats = []
        for i in range(30):
            date = today - timedelta(days=i)
            visitors_count = Visitor.objects.filter(first_visit__date=date).count()
            page_views_count = PageView.objects.filter(timestamp__date=date).count()
            daily_stats.append({
                'date': date.strftime('%Y-%m-%d'),
                'visitors': visitors_count,
                'page_views': page_views_count
            })
        
        daily_stats.reverse()  # ترتيب تصاعدي
        
        # معدل التحويل (النقرات مقسومة على الزوار)
        conversion_rate = (total_clicks / total_visitors * 100) if total_visitors > 0 else 0
        
        # متوسط مدة الجلسة
        avg_session = Visitor.objects.aggregate(
            avg_duration=Avg('session_duration')
        )['avg_duration'] or 0
        
        # الزوار العائدون
        returning_visitors = Visitor.objects.filter(visit_count__gt=1).count()
        returning_rate = (returning_visitors / total_visitors * 100) if total_visitors > 0 else 0
        
        context = {
            'title': 'إحصائيات الموقع المفصلة',
            'total_visitors': total_visitors,
            'total_page_views': total_page_views,
            'total_clicks': total_clicks,
            'today_visitors': today_visitors,
            'today_page_views': today_page_views,
            'today_clicks': today_clicks,
            'weekly_visitors': weekly_visitors,
            'monthly_visitors': monthly_visitors,
            'device_stats': device_stats,
            'popular_pages': popular_pages,
            'popular_buttons': popular_buttons,
            'daily_stats_json': json.dumps(daily_stats),
            'conversion_rate': round(conversion_rate, 2),
            'avg_session': round(avg_session / 60, 2) if avg_session else 0,  # بالدقائق
            'returning_rate': round(returning_rate, 2),
            'returning_visitors': returning_visitors,
        }
        
        return render(request, 'admin/statistics.html', context)
    
    def index(self, request, extra_context=None):
        """
        تخصيص الصفحة الرئيسية للإدارة
        """
        extra_context = extra_context or {}
        
        # إضافة إحصائيات سريعة للصفحة الرئيسية
        extra_context.update({
            'quick_stats': {
                'total_visitors': Visitor.objects.count(),
                'today_visitors': Visitor.objects.filter(
                    first_visit__date=timezone.now().date()
                ).count(),
                'total_page_views': PageView.objects.count(),
                'total_clicks': ClickEvent.objects.count(),
            }
        })
        
        return super().index(request, extra_context)


# استخدام الموقع المخصص
admin_site = CustomAdminSite(name='custom_admin')

# تسجيل النماذج
admin_site.register(Visitor, VisitorAdmin)
admin_site.register(PageView, PageViewAdmin)
admin_site.register(ClickEvent, ClickEventAdmin)
admin_site.register(DailyStats, DailyStatsAdmin)
admin_site.register(ContactMessage, ContactMessageAdmin)

# تسجيل النماذج في الإدارة الافتراضية أيضاً
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(ClickEvent, ClickEventAdmin)
admin.site.register(DailyStats, DailyStatsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
