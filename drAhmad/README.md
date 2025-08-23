# 🌟 الدكتور أحمد أبو صفية - موقع محلل مالي

موقع احترافي للدكتور أحمد أبو صفية، محلل مالي متخصص، مبني بـ Django مع تصميم عصري ومتجاوب.

## 🚀 المميزات

- ✨ تصميم فاخر بألوان الأسود والذهبي
- 📱 تصميم متجاوب يعمل على جميع الأجهزة
- ⚡ تأثيرات بصرية احترافية وحركات سلسة
- 🎯 أربع خدمات مالية متخصصة
- 🔗 ربط مباشر لفتح حساب تداول
- 🌐 دعم كامل للغة العربية

## 🛠️ التقنيات المستخدمة

- **Backend**: Django 4.2.23
- **Frontend**: HTML5, CSS3, JavaScript
- **التصميم**: CSS Grid, Flexbox, Animations
- **الخطوط**: Tajawal (Google Fonts)
- **الأيقونات**: Font Awesome 6.0

## 📦 التثبيت والتشغيل

### 1. تحميل المشروع
```bash
git clone <repository-url>
cd drAhmad
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. تطبيق قاعدة البيانات
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. تشغيل الخادم
```bash
python manage.py runserver
```

### 6. الوصول للموقع
افتح المتصفح واذهب إلى: http://127.0.0.1:8000/

## 📁 هيكل المشروع

```
drAhmad/
├── drAhmad/                 # إعدادات المشروع الرئيسي
│   ├── __init__.py
│   ├── settings.py          # إعدادات Django
│   ├── urls.py             # مسارات URL الرئيسية
│   ├── wsgi.py
│   └── asgi.py
├── landing/                 # تطبيق الصفحة الرئيسية
│   ├── templates/
│   │   └── landing/
│   │       └── index.html   # قالب الصفحة الرئيسية
│   ├── views.py            # عروض Django
│   ├── urls.py             # مسارات التطبيق
│   ├── models.py
│   ├── admin.py
│   └── apps.py
├── static/                  # الملفات الثابتة
│   ├── css/
│   │   └── styles.css      # ملف التنسيقات الرئيسي
│   ├── js/
│   │   └── script.js       # ملف JavaScript
│   └── images/
│       ├── abo.png         # صورة الدكتور أحمد
│       └── logo.png        # شعار T4T Trading
├── requirements.txt         # متطلبات المشروع
├── manage.py               # أداة إدارة Django
└── README.md              # هذا الملف
```

## 🎨 الخدمات المعروضة

1. **إستراتيجية أبو صفية** - استراتيجية تداول مبتكرة ومجربة
2. **لايف على التليجرام** - تحليلات مباشرة وتوصيات فورية
3. **صفقات داخلية** - فرص استثمارية حصرية
4. **ربط حسابك بـ MT5** - ربط آمن مع منصة MetaTrader 5

## 🔧 التخصيص

### تغيير الألوان
عدّل المتغيرات في `static/css/styles.css`:
```css
:root {
    --primary-color: #1a1a2e;
    --accent-color: #ffd700;
    /* باقي المتغيرات... */
}
```

### إضافة خدمات جديدة
عدّل قائمة `services` في `landing/views.py`:
```python
'services': [
    {
        'title': 'خدمة جديدة',
        'description': 'وصف الخدمة',
        'icon': 'fas fa-icon-name'
    }
]
```

## 🌐 النشر

### Heroku
```bash
pip install gunicorn
# إضافة Procfile
echo "web: gunicorn drAhmad.wsgi" > Procfile
```

### VPS/Dedicated Server
```bash
pip install gunicorn whitenoise
python manage.py collectstatic
gunicorn drAhmad.wsgi:application
```

## 📞 التواصل

- **الموقع**: [رابط فتح الحساب](https://signup.4t.com/ar/?utm_source=IB&utm_medium=Direct&link_id=vuygz25660&referral_id=0023161)
- **التليجرام**: [قناة التليجرام]
- **واتساب**: [رقم الواتساب]

## 📝 الترخيص

جميع الحقوق محفوظة © 2024 الدكتور أحمد أبو صفية

---

**تم تطوير هذا المشروع بـ ❤️ باستخدام Django**

