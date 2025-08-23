from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Visitor(models.Model):
    """
    نموذج لتتبع زوار الموقع
    """
    # معرف فريد للزائر (باستخدام الكوكيز أو الجلسة)
    visitor_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    
    # عنوان IP للزائر
    ip_address = models.GenericIPAddressField()
    
    # معلومات المتصفح
    user_agent = models.TextField(blank=True, null=True)
    
    # الصفحة المزارة
    page_visited = models.CharField(max_length=200, default='/')
    
    # معلومات الإحالة
    referrer = models.URLField(blank=True, null=True)
    
    # الدولة (اختياري)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # المدينة (اختياري)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # نوع الجهاز
    device_type = models.CharField(max_length=50, choices=[
        ('desktop', 'سطح المكتب'),
        ('mobile', 'جوال'),
        ('tablet', 'تابلت'),
        ('unknown', 'غير معروف')
    ], default='unknown')
    
    # تاريخ ووقت الزيارة الأولى
    first_visit = models.DateTimeField(default=timezone.now)
    
    # تاريخ ووقت آخر زيارة
    last_visit = models.DateTimeField(auto_now=True)
    
    # عدد الزيارات
    visit_count = models.PositiveIntegerField(default=1)
    
    # مدة البقاء في الموقع (بالثواني)
    session_duration = models.PositiveIntegerField(default=0)
    
    # هل الزائر مهتم (تفاعل مع الأزرار)
    is_engaged = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'زائر'
        verbose_name_plural = 'الزوار'
        ordering = ['-last_visit']
    
    def __str__(self):
        return f"زائر {self.ip_address} - {self.visit_count} زيارة"
    
    @property
    def is_returning_visitor(self):
        """هل الزائر عائد؟"""
        return self.visit_count > 1
    
    @property
    def time_since_first_visit(self):
        """الوقت منذ أول زيارة"""
        return timezone.now() - self.first_visit


class PageView(models.Model):
    """
    نموذج لتتبع مشاهدات الصفحات
    """
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='page_views')
    page_url = models.CharField(max_length=200)
    page_title = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    time_spent = models.PositiveIntegerField(default=0)  # بالثواني
    
    class Meta:
        verbose_name = 'مشاهدة صفحة'
        verbose_name_plural = 'مشاهدات الصفحات'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.page_url} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class ClickEvent(models.Model):
    """
    نموذج لتتبع النقرات على الأزرار المهمة
    """
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='clicks')
    element_clicked = models.CharField(max_length=100, choices=[
        ('cta_primary', 'زر فتح الحساب الرئيسي'),
        ('cta_secondary', 'زر اكتشف خدماتنا'),
        ('cta_large', 'زر فتح الحساب الكبير'),
        ('social_telegram', 'رابط التليجرام'),
        ('social_whatsapp', 'رابط الواتساب'),
        ('social_instagram', 'رابط الانستجرام'),
        ('nav_services', 'رابط الخدمات في التنقل'),
    ])
    timestamp = models.DateTimeField(default=timezone.now)
    page_url = models.CharField(max_length=200, default='/')
    
    class Meta:
        verbose_name = 'نقرة'
        verbose_name_plural = 'النقرات'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_element_clicked_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class DailyStats(models.Model):
    """
    إحصائيات يومية مجمعة
    """
    date = models.DateField(unique=True, default=timezone.now)
    unique_visitors = models.PositiveIntegerField(default=0)
    total_page_views = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    avg_session_duration = models.FloatField(default=0.0)
    bounce_rate = models.FloatField(default=0.0)  # معدل الارتداد
    conversion_rate = models.FloatField(default=0.0)  # معدل التحويل
    
    class Meta:
        verbose_name = 'إحصائيات يومية'
        verbose_name_plural = 'الإحصائيات اليومية'
        ordering = ['-date']
    
    def __str__(self):
        return f"إحصائيات {self.date.strftime('%Y-%m-%d')}"


class ContactMessage(models.Model):
    """
    نموذج لحفظ رسائل التواصل
    """
    SERVICE_CHOICES = [
        ('strategy', 'إستراتيجية أبو صفية'),
        ('telegram', 'لايف على التليجرام'),
        ('internal-deals', 'صفقات داخلية'),
        ('mt5-connection', 'ربط حساب MT5'),
        ('', 'غير محدد'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='الاسم الكامل')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='رقم الهاتف')
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True, verbose_name='الخدمة المطلوبة')
    message = models.TextField(verbose_name='الرسالة')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاريخ الإرسال')
    is_read = models.BooleanField(default=False, verbose_name='تم القراءة')
    
    class Meta:
        verbose_name = 'رسالة تواصل'
        verbose_name_plural = 'رسائل التواصل'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"رسالة من {self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"