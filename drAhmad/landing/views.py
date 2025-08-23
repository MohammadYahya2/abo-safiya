from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from datetime import datetime, timedelta
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from .models import Visitor, ClickEvent, PageView, DailyStats, ContactMessage
from .stats_views import statistics_dashboard
import json

def index(request):
    """
    عرض الصفحة الرئيسية للدكتور أحمد أبو صفية
    """
    context = {
        'page_title': 'الدكتور أحمد أبو صفية - محلل مالي',
        'services': [
            {
                'title': 'إستراتيجية أبو صفية',
                'description': 'استراتيجية تداول مبتكرة ومجربة تعتمد على التحليل الفني والأساسي',
                'icon': 'fas fa-chess-king'
            },
            {
                'title': 'لايف على التليجرام',
                'description': 'تحليلات مباشرة وتوصيات فورية عبر قناة التليجرام',
                'icon': 'fab fa-telegram'
            },
            {
                'title': 'صفقات داخلية',
                'description': 'فرص استثمارية حصرية وصفقات مدروسة بعناية',
                'icon': 'fas fa-handshake'
            },
            {
                'title': 'ربط حسابك بــ MT5',
                'description': 'ربط سهل وآمن لحسابك مع منصة MetaTrader 5',
                'icon': 'fas fa-link'
            }
        ]
    }
    return render(request, 'landing/index.html', context)


@csrf_exempt
@require_POST
def track_click(request):
    """
    تتبع النقرات على الأزرار المهمة
    """
    try:
        data = json.loads(request.body)
        element_clicked = data.get('element_clicked')
        page_url = data.get('page_url', '/')
        
        # الحصول على الزائر من الجلسة
        visitor = getattr(request, 'visitor', None)
        
        if visitor and element_clicked:
            # إنشاء سجل النقرة
            ClickEvent.objects.create(
                visitor=visitor,
                element_clicked=element_clicked,
                page_url=page_url
            )
            
            # تحديث حالة الاهتمام للزائر
            visitor.is_engaged = True
            visitor.save()
            
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'status': 'error', 'message': 'Missing data'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@csrf_exempt
@require_POST
def update_session(request):
    """
    تحديث مدة الجلسة للزائر
    """
    try:
        data = json.loads(request.body)
        session_duration = data.get('session_duration', 0)
        
        # الحصول على الزائر من الجلسة
        visitor = getattr(request, 'visitor', None)
        
        if visitor and session_duration > 0:
            # تحديث مدة الجلسة (إضافة الوقت الجديد)
            visitor.session_duration += session_duration
            visitor.save()
            
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'status': 'error', 'message': 'Missing data'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def contact_submit(request):
    """
    معالجة نموذج التواصل وإرسال البريد الإلكتروني
    """
    if request.method == 'POST':
        try:
            # استخراج البيانات من النموذج
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            service = request.POST.get('service', '').strip()
            message = request.POST.get('message', '').strip()
            
            # التحقق من البيانات المطلوبة
            if not name or not email or not message:
                messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
                return redirect('/#contact')
            
            # حفظ الرسالة في قاعدة البيانات
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                service=service,
                message=message
            )
            
            # إعداد محتوى البريد الإلكتروني
            service_display = dict(ContactMessage.SERVICE_CHOICES).get(service, 'غير محدد')
            
            email_subject = f'📧 رسالة جديدة من {name} - موقع الدكتور أحمد أبو صفية'
            
            # إعداد السياق للقالب
            email_context = {
                'name': name,
                'email': email,
                'phone': phone,
                'service_display': service_display,
                'message': message,
                'created_at': contact_message.created_at,
            }
            
            # إنشاء محتوى HTML من القالب
            html_content = render_to_string('landing/email_template.html', email_context)
            
            # إنشاء نسخة نصية بسيطة
            text_content = f"""
رسالة جديدة من موقع الدكتور أحمد أبو صفية

الاسم: {name}
البريد الإلكتروني: {email}
رقم الهاتف: {phone if phone else 'لم يتم تقديمه'}
الخدمة المطلوبة: {service_display}

الرسالة:
{message}

تاريخ الإرسال: {contact_message.created_at.strftime('%d/%m/%Y - %H:%M')}
            """
            
            # إرسال البريد الإلكتروني
            try:
                # إنشاء بريد إلكتروني مع دعم HTML و TEXT
                email_message = EmailMultiAlternatives(
                    subject=email_subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.ADMIN_EMAIL],
                )
                
                # إضافة المحتوى HTML
                email_message.attach_alternative(html_content, "text/html")
                
                # إرسال البريد
                email_message.send(fail_silently=False)
                
                # رسالة نجاح
                messages.success(request, '✅ تم إرسال رسالتك بنجاح! سيتم التواصل معك قريباً.')
                
            except Exception as email_error:
                # في حالة فشل إرسال البريد، سجل الخطأ لكن أظهر رسالة نجاح للمستخدم
                print(f"Email sending failed: {email_error}")
                messages.success(request, '📝 تم استلام رسالتك وحفظها! سيتم التواصل معك قريباً.')
            
        except Exception as e:
            print(f"Contact form error: {e}")
            messages.error(request, 'حدث خطأ أثناء إرسال الرسالة. يرجى المحاولة مرة أخرى.')
    
    return redirect('/#contact')


def email_preview(request):
    """
    معاينة تصميم البريد الإلكتروني (للاختبار فقط)
    """
    # بيانات تجريبية لمعاينة التصميم
    email_context = {
        'name': 'أحمد محمد السعدي',
        'email': 'ahmed.saadi@example.com',
        'phone': '0599123456',
        'service_display': 'إستراتيجية أبو صفية',
        'message': 'السلام عليكم دكتور أحمد، أريد أن أتعلم استراتيجية التداول الخاصة بك وأشترك في الدورة التدريبية. لدي خبرة بسيطة في التداول وأريد تطوير مهاراتي.',
        'created_at': timezone.now(),
    }
    
    return render(request, 'landing/email_template.html', email_context)
