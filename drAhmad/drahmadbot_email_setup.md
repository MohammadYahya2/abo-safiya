# 📧 إعداد البريد الإلكتروني لموقع drahmadbot.site

## 🎯 **الخطوات المطلوبة:**

### **الخطوة 1: إنشاء إيميل في cPanel**

1. **ادخل على cPanel** الخاص بـ drahmadbot.site
2. **اذهب إلى "Email Accounts"**
3. **اضغط "Create"**
4. **أنشئ الإيميلات التالية:**
   - `noreply@drahmadbot.site` (للإرسال)
   - `contact@drahmadbot.site` (بديل)
5. **ضع كلمة مرور قوية**
6. **احفظ كلمة المرور** لأنك ستحتاجها في الكود

### **الخطوة 2: تحديث إعدادات Django**

```python
# في settings.py (محدث بالفعل)
EMAIL_HOST_USER = 'noreply@drahmadbot.site'
EMAIL_HOST_PASSWORD = 'كلمة_المرور_التي_أنشأتها'
DEFAULT_FROM_EMAIL = 'noreply@drahmadbot.site'
ADMIN_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'
```

### **الخطوة 3: معرفة إعدادات SMTP**

في cPanel:
1. **اذهب لـ "Email Accounts"**
2. **اضغط "Connect Devices"** جنب الإيميل
3. **انسخ إعدادات SMTP:**

```python
# إعدادات محتملة لـ drahmadbot.site:
EMAIL_HOST = 'mail.drahmadbot.site'
EMAIL_PORT = 587  # أو 465
EMAIL_USE_TLS = True  # أو False
```

### **الخطوة 4: تطبيق الإعدادات**

```python
# في settings.py - غير هذه الإعدادات حسب ما تجده في cPanel:
EMAIL_HOST = 'mail.drahmadbot.site'  # بدلاً من localhost
EMAIL_HOST_USER = 'noreply@drahmadbot.site'
EMAIL_HOST_PASSWORD = 'كلمة_المرور_الفعلية'
```

## 🧪 **اختبار الإعدادات:**

```bash
python manage.py test_email
```

## 📋 **قائمة مرجعية:**

- [x] ✅ الدومين معروف: drahmadbot.site
- [x] ✅ الكود محدث للدومين الجديد
- [ ] ⏳ إنشاء إيميل noreply@drahmadbot.site
- [ ] ⏳ معرفة كلمة المرور
- [ ] ⏳ معرفة إعدادات SMTP من cPanel
- [ ] ⏳ تحديث EMAIL_HOST_PASSWORD
- [ ] ⏳ اختبار الإرسال

## 🔄 **إعدادات بديلة:**

### **إذا لم تعمل الطريقة الأولى:**

```python
# جرب إعدادات مختلفة:
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
```

### **أو:**

```python
EMAIL_HOST = 'smtp.drahmadbot.site'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
```

## 🚀 **SendGrid كحل سريع:**

إذا كانت الاستضافة تحجب SMTP:

1. **سجل في SendGrid:** https://sendgrid.com
2. **احصل على API Key مجاني**
3. **استخدم:**

```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'SG.xxxxxxxxxxxxxxxxxxxxxxxx'
```

## 📞 **اتصل بشركة الاستضافة:**

إذا لم تنجح الطرق السابقة:

**قل لهم:**
"أريد إرسال emails من Python/Django على drahmadbot.site، ما هي إعدادات SMTP المطلوبة؟"

**اطلب منهم:**
- SMTP Server Name
- Port Number (587, 465, 25)
- TLS/SSL Settings
- Authentication Requirements

---

## ✅ **النتيجة المتوقعة:**

بعد تطبيق هذه الخطوات:
- ✅ الرسائل ستصل لـ Dr.ahmadabusaffia608@gmail.com
- ✅ المرسل سيظهر: noreply@drahmadbot.site  
- ✅ التصميم HTML الجميل سيعمل
- ✅ جميع الرسائل محفوظة في قاعدة البيانات

الموقع جميل جداً على drahmadbot.site! 🎉
الآن فقط نحتاج إعداد البريد ليكتمل كل شيء! 🚀
