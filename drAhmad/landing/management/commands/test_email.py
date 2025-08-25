from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
import smtplib
import socket


class Command(BaseCommand):
    help = 'اختبار إعدادات البريد الإلكتروني'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 بدء اختبار إعدادات البريد الإلكتروني...'))
        
        # 1. التحقق من الإعدادات
        self.test_settings()
        
        # 2. اختبار الاتصال بالخادم
        self.test_connection()
        
        # 3. اختبار إرسال بريد بسيط
        self.test_simple_email()
        
        # 4. اختبار إرسال بريد HTML
        self.test_html_email()

    def test_settings(self):
        self.stdout.write('\n📋 فحص الإعدادات:')
        
        settings_to_check = [
            ('EMAIL_BACKEND', settings.EMAIL_BACKEND),
            ('EMAIL_HOST', settings.EMAIL_HOST),
            ('EMAIL_PORT', settings.EMAIL_PORT),
            ('EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
            ('EMAIL_HOST_USER', settings.EMAIL_HOST_USER),
            ('EMAIL_HOST_PASSWORD', '***' if settings.EMAIL_HOST_PASSWORD else 'غير موجود'),
            ('DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL),
            ('ADMIN_EMAIL', settings.ADMIN_EMAIL),
        ]
        
        for setting_name, setting_value in settings_to_check:
            self.stdout.write(f'  ✅ {setting_name}: {setting_value}')

    def test_connection(self):
        self.stdout.write('\n🔌 اختبار الاتصال بخادم SMTP:')
        
        try:
            # محاولة الاتصال بخادم Gmail
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.quit()
            
            self.stdout.write(self.style.SUCCESS('  ✅ تم الاتصال بنجاح!'))
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ في المصادقة: {e}'))
        except smtplib.SMTPConnectError as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ في الاتصال: {e}'))
        except smtplib.SMTPException as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ SMTP: {e}'))
        except socket.gaierror as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ في DNS/الشبكة: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ غير متوقع: {e}'))
        
        return False

    def test_simple_email(self):
        self.stdout.write('\n📧 اختبار إرسال بريد بسيط:')
        
        try:
            result = send_mail(
                subject='اختبار البريد الإلكتروني - موقع الدكتور أحمد',
                message=f'هذا اختبار للبريد الإلكتروني من موقع الدكتور أحمد أبو صفية.\n\nالتاريخ: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            if result == 1:
                self.stdout.write(self.style.SUCCESS('  ✅ تم إرسال البريد البسيط بنجاح!'))
                return True
            else:
                self.stdout.write(self.style.ERROR('  ❌ فشل إرسال البريد البسيط'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ في إرسال البريد البسيط: {e}'))
        
        return False

    def test_html_email(self):
        self.stdout.write('\n🎨 اختبار إرسال بريد HTML:')
        
        try:
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; direction: rtl;">
                <h2 style="color: #1a1a2e;">اختبار البريد الإلكتروني HTML</h2>
                <p>هذا اختبار لإرسال بريد HTML من موقع الدكتور أحمد أبو صفية.</p>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <strong>تفاصيل الاختبار:</strong><br>
                    التاريخ: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
                    الخادم: {settings.EMAIL_HOST}<br>
                    المرسل: {settings.EMAIL_HOST_USER}
                </div>
                <p style="color: #28a745;">✅ إذا وصلتك هذه الرسالة، فإن إعدادات البريد الإلكتروني تعمل بشكل صحيح!</p>
            </body>
            </html>
            """
            
            text_content = f"""
اختبار البريد الإلكتروني - موقع الدكتور أحمد أبو صفية

هذا اختبار لإرسال بريد HTML من الموقع.

تفاصيل الاختبار:
التاريخ: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}
الخادم: {settings.EMAIL_HOST}
المرسل: {settings.EMAIL_HOST_USER}

إذا وصلتك هذه الرسالة، فإن إعدادات البريد الإلكتروني تعمل بشكل صحيح!
            """
            
            email_message = EmailMultiAlternatives(
                subject='اختبار البريد HTML - موقع الدكتور أحمد',
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            
            email_message.attach_alternative(html_content, "text/html")
            result = email_message.send(fail_silently=False)
            
            if result == 1:
                self.stdout.write(self.style.SUCCESS('  ✅ تم إرسال البريد HTML بنجاح!'))
                return True
            else:
                self.stdout.write(self.style.ERROR('  ❌ فشل إرسال البريد HTML'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ خطأ في إرسال البريد HTML: {e}'))
        
        return False

    def add_arguments(self, parser):
        parser.add_argument(
            '--quick',
            action='store_true',
            help='اختبار سريع بدون إرسال بريد فعلي',
        )
