# 🔧 إعداد البريد الإلكتروني لـ cPanel

## المشكلة: 
الكود يعمل على localhost بس ما بيشتغل على cPanel

## 🎯 **الحل الصحيح:**

### **الخطوة 1: إنشاء إيميل من نفس الدومين**

#### في cPanel:
1. اذهب إلى **"Email Accounts"**
2. اضغط **"Create"** 
3. أنشئ إيميل مثل: `noreply@yourdomain.com`
4. أو: `contact@yourdomain.com`
5. احفظ كلمة المرور

### **الخطوة 2: تحديث إعدادات Django**

```python
# في settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'  # أو mail.yourdomain.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourdomain.com'  # الإيميل الجديد
EMAIL_HOST_PASSWORD = 'password_you_created'  # كلمة المرور
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'  # من هذا الإيميل
ADMIN_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'  # إلى هذا الإيميل
```

### **الخطوة 3: أو استخدم إعدادات الاستضافة**

```python
# إعدادات شائعة لاستضافات cPanel
EMAIL_HOST = 'mail.yourdomain.com'
EMAIL_PORT = 587  # أو 465
EMAIL_USE_TLS = True  # أو False
EMAIL_USE_SSL = False  # أو True للـ 465
```

## 🔍 **طريقة معرفة إعدادات السيرفر:**

### في cPanel:
1. اذهب إلى **"Email Accounts"**
2. اضغط **"Connect Devices"** جنب الإيميل
3. ستجد إعدادات SMTP:
   - **Incoming Server:** mail.yourdomain.com
   - **Outgoing Server:** mail.yourdomain.com  
   - **Port:** 587 أو 465
   - **Security:** TLS أو SSL

## 📧 **البديل السريع: SendGrid**

إذا لم تنجح الطريقة السابقة:

1. **سجل في SendGrid:** https://sendgrid.com (مجاني)
2. **احصل على API Key**
3. **غير الإعدادات:**

```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'YOUR_SENDGRID_API_KEY'
```

## 🧪 **اختبار الإعدادات:**

```bash
python manage.py test_email
```

## ✅ **الإعدادات الصحيحة الآن:**

الكود محدث ليجرب 3 طرق:
1. **SMTP السيرفر** (الأفضل لـ cPanel)
2. **إرسال بسيط** (backup)
3. **Gmail** (للطوارئ)

ويحفظ في قاعدة البيانات أي طريقة نجحت!

---

## 📞 **إذا ما زال لا يعمل:**

**اتصل بشركة الاستضافة وقل:**
- "أريد إرسال emails من Python/Django"
- "ما هي إعدادات SMTP المطلوبة؟"
- "هل تدعمون outgoing SMTP؟"

معظم الاستضافات تعطيك الإعدادات الصحيحة فوراً! 🚀
