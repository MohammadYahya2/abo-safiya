# 🔧 دليل تشخيص مشاكل البريد الإلكتروني

## 🚨 **المشكلة:** البريد الإلكتروني لا يصل على السيرفر

### 📋 **خطوات التشخيص:**

## 1. **اختبار إعدادات البريد محلياً**

```bash
# تشغيل أداة التشخيص
python manage.py test_email
```

## 2. **التحقق من إعدادات Gmail**

### ✅ **تأكد من:**
- [x] تم تفعيل المصادقة الثنائية
- [x] تم إنشاء كلمة مرور التطبيق
- [x] كلمة المرور صحيحة: `aetr ejjm hpwy giww`

### 🔑 **إعداد كلمة مرور التطبيق:**
1. اذهب إلى: https://myaccount.google.com/
2. الأمان → التحقق بخطوتين
3. كلمات مرور التطبيقات
4. اختر "التطبيقات والأجهزة الأخرى"
5. أدخل "Django Website"
6. انسخ كلمة المرور المكونة من 16 حرف

## 3. **مشاكل السيرفر الشائعة**

### 🔧 **إعدادات الاستضافة:**

#### **أ) Shared Hosting:**
```python
# قد تحتاج لتغيير إعدادات SMTP
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # بدلاً من 587
EMAIL_USE_SSL = True  # بدلاً من TLS
EMAIL_USE_TLS = False
```

#### **ب) VPS/Dedicated Server:**
```bash
# تحقق من Port 587 مفتوح
telnet smtp.gmail.com 587

# تحقق من Port 465 مفتوح  
telnet smtp.gmail.com 465
```

#### **ج) Docker/Cloud:**
```python
# قد تحتاج لإعدادات شبكة إضافية
EMAIL_TIMEOUT = 60  # زيادة وقت الانتظار
```

## 4. **بدائل Gmail للسيرفر**

### 📧 **استخدام SendGrid (مجاني):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'YOUR_SENDGRID_API_KEY'
```

### 📧 **استخدام Mailgun:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'YOUR_MAILGUN_USERNAME'
EMAIL_HOST_PASSWORD = 'YOUR_MAILGUN_PASSWORD'
```

## 5. **فحص Logs على السيرفر**

### 📊 **في Django:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# في views.py سيطبع تفاصيل الأخطاء
```

### 📊 **في cPanel/WHM:**
- Error Logs
- Email Logs
- PHP Error Logs

## 6. **حل مؤقت: استخدام خدمة خارجية**

### 🚀 **EmailJS (للبريد المباشر من الموقع):**
```html
<!-- في template -->
<script src="https://cdn.emailjs.com/user/YOUR_USER_ID/sdk/emailjs-sdk.min.js"></script>
<script>
emailjs.sendForm('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', this)
</script>
```

## 7. **اختبار المشكلة خطوة بخطوة**

### 🔍 **على السيرفر:**
```bash
# 1. اختبر إعدادات البريد
python manage.py test_email

# 2. تحقق من الشبكة
ping smtp.gmail.com

# 3. تحقق من Port
telnet smtp.gmail.com 587

# 4. فحص Django logs
tail -f /path/to/django/logs/error.log
```

## 8. **إعدادات السيرفر المطلوبة**

### ⚙️ **في PHP.ini أو Apache:**
```apache
# السماح بإرسال البريد
allow_url_fopen = On
allow_url_include = On

# إعدادات SMTP
SMTP = smtp.gmail.com
smtp_port = 587
```

### ⚙️ **في WHM/cPanel:**
- تفعيل "Exim Mail Server"
- إعداد "SMTP Authentication"
- فتح Ports: 587, 465, 25

## 9. **رسائل الخطأ الشائعة وحلولها**

### ❌ **"Authentication failed"**
- تحقق من كلمة مرور التطبيق
- تأكد من تفعيل المصادقة الثنائية

### ❌ **"Connection timeout"**
- تحقق من إعدادات Firewall
- جرب Port 465 بدلاً من 587

### ❌ **"Permission denied"**
- تحقق من صلاحيات السيرفر
- تواصل مع مزود الاستضافة

## 10. **خطة البديل السريع**

### 📞 **Webhook إلى WhatsApp:**
```python
import requests

def send_whatsapp_notification(message):
    # استخدام خدمة WhatsApp API
    url = "https://api.whatsapp.com/send"
    # تنفيذ إرسال إشعار
```

### 📧 **حفظ في قاعدة البيانات فقط:**
```python
# في views.py - إضافة إشعار للأدمن
contact_message.admin_notified = False
contact_message.save()

# صفحة خاصة لعرض الرسائل الجديدة
```

## 📞 **تواصل مع مزود الاستضافة**

إذا لم تنجح الحلول السابقة، تواصل مع مزود الاستضافة وأخبرهم:

1. **تريد إرسال SMTP emails من Django**
2. **تستخدم Gmail SMTP**
3. **Ports المطلوبة: 587, 465**
4. **تحتاج تفعيل outgoing SMTP**

---

## ✅ **الحل الآن مطبق:**

- ✅ إعدادات محسنة للبريد الإلكتروني
- ✅ تشخيص الأخطاء وحفظها
- ✅ أداة اختبار: `python manage.py test_email`
- ✅ fallback system في حالة فشل الإرسال
- ✅ تتبع حالة البريد في لوحة الإدارة

استخدم `python manage.py test_email` لاختبار إعدادات البريد على السيرفر! 🚀
