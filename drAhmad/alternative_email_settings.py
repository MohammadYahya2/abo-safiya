# إعدادات بديلة للبريد الإلكتروني - جرب واحدة تلو الأخرى

# الخيار 1: Gmail مع SSL (Port 465)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'Dr.ahmadabusaffia608@gmail.com'
EMAIL_HOST_PASSWORD = 'aetr ejjm hpwy giww'
DEFAULT_FROM_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'
ADMIN_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'
EMAIL_TIMEOUT = 60

# الخيار 2: Gmail مع TLS محسن
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'Dr.ahmadabusaffia608@gmail.com'
EMAIL_HOST_PASSWORD = 'aetr ejjm hpwy giww'
DEFAULT_FROM_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'
ADMIN_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'
EMAIL_TIMEOUT = 60
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None

# الخيار 3: SendGrid (مجاني وموثوق للسيرفرات)
# سجل في: https://sendgrid.com
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'aetr ejjm hpwy giww'  # ضع API key هنا
DEFAULT_FROM_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'
ADMIN_EMAIL = 'Dr.ahmadabusaffia608@gmail.com'

# الخيار 4: للاختبار المحلي فقط (يحفظ في console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# الخيار 5: للاختبار (يحفظ في ملف)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'  # للينكس
# EMAIL_FILE_PATH = 'C:/temp/app-messages'  # للويندوز
