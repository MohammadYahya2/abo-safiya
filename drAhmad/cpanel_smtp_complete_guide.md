# 📧 الدليل الكامل لإعداد SMTP مع cPanel

## 🎯 **الهدف:** إرسال إيميلات من drahmadbot.site بدون خدمات خارجية

---

## 📋 **الخطوة 1: إنشاء إيميل في cPanel**

### **ادخل على cPanel:**
1. **اذهب إلى cPanel** الخاص بـ drahmadbot.site
2. **ابحث عن "Email Accounts"**
3. **اضغط "Create"**

### **أنشئ الإيميل:**
- **Email:** noreply@drahmadbot.site
- **Password:** (كلمة مرور قوية - احفظها!)
- **Storage:** 250 MB (كافي)

### **أو جرب إيميلات أخرى:**
- contact@drahmadbot.site
- admin@drahmadbot.site
- info@drahmadbot.site

---

## 🔧 **الخطوة 2: معرفة إعدادات SMTP**

### **في cPanel:**
1. **اذهب إلى Email Accounts**
2. **اضغط "Connect Devices"** جنب الإيميل الجديد
3. **انسخ إعدادات SMTP:**

```
Incoming Server: mail.drahmadbot.site
Outgoing Server: mail.drahmadbot.site
Port: 587 (أو 465 أو 25)
Security: TLS (أو SSL أو None)
```

---

## ⚙️ **الخطوة 3: تحديث إعدادات Django**

### **في settings.py غير:**
```python
EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_PASSWORD_HERE'
```

**إلى كلمة المرور الفعلية التي أنشأتها**

### **إذا لم تعمل، جرب هذه الإعدادات واحدة تلو الأخرى:**

#### **🔄 التجربة 1: الإعداد العادي**
```python
EMAIL_HOST = 'mail.drahmadbot.site'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

#### **🔄 التجربة 2: localhost**
```python
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
```

#### **🔄 التجربة 3: SSL**
```python
EMAIL_HOST = 'mail.drahmadbot.site'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
```

#### **🔄 التجربة 4: SMTP مباشر**
```python
EMAIL_HOST = 'smtp.drahmadbot.site'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

---

## 🧪 **الخطوة 4: اختبار كل إعداد**

بعد كل تغيير، اختبر:
```bash
python manage.py test_email
```

---

## 📞 **الخطوة 5: إذا لم تعمل - اتصل بالدعم**

**اتصل بشركة الاستضافة وقل:**

> "مرحباً، أريد إرسال emails من موقع drahmadbot.site باستخدام Python/Django. 
> 
> **ما هي إعدادات SMTP الصحيحة؟**
> 
> - SMTP Server Name؟
> - Port Number؟ 
> - TLS أم SSL؟
> - هل تدعمون outgoing SMTP؟"

**سيعطوك الإعدادات الصحيحة فوراً!**

---

## 🔄 **بدائل سريعة أخرى:**

### **1. Mailgun (مجاني 300 إيميل شهرياً):**
```python
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@mg.drahmadbot.site'
EMAIL_HOST_PASSWORD = 'mailgun-api-key'
```

### **2. Mailtrap (للاختبار فقط):**
```python
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mailtrap-username'
EMAIL_HOST_PASSWORD = 'mailtrap-password'
```

### **3. SMTP2GO (مجاني 1000 إيميل شهرياً):**
```python
EMAIL_HOST = 'mail.smtp2go.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'smtp2go-username'
EMAIL_HOST_PASSWORD = 'smtp2go-password'
```

---

## ✅ **الأولوية:**

1. **🥇 إيميل الاستضافة** (noreply@drahmadbot.site)
2. **🥈 localhost** مع Port 25
3. **🥉 Mailgun** (مجاني وموثوق)
4. **🏅 SMTP2GO** (بديل ممتاز)

---

## 🎯 **النتيجة المتوقعة:**

- ✅ **المرسل:** noreply@drahmadbot.site
- ✅ **المستقبل:** Dr.ahmadabusaffia608@gmail.com
- ✅ **التصميم:** HTML جميل مع اللوغو
- ✅ **الموثوقية:** 99% نجاح

**جرب الخطوات بالترتيب وستحل المشكلة 100%!** 🚀
