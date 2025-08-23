from django.shortcuts import render


def strategy_details(request):
    """
    صفحة تفاصيل إستراتيجية أبو صفية
    """
    context = {
        'page_title': 'إستراتيجية أبو صفية - تفاصيل الخدمة',
        'service_name': 'إستراتيجية أبو صفية',
        'service_icon': 'fas fa-chess-king',
        'description': 'استراتيجية تداول مبتكرة ومجربة تعتمد على التحليل الفني والأساسي لتحقيق أفضل النتائج في الأسواق المالية.',
        'features': [
            'تحليل فني متقدم باستخدام المؤشرات الرائدة',
            'تحليل أساسي شامل للأسواق العالمية',
            'إدارة المخاطر الاحترافية',
            'خطط استثمارية مخصصة لكل عميل',
            'متابعة يومية للصفقات والمحافظ',
            'تدريب شخصي على الاستراتيجية'
        ],
        'benefits': [
            'عوائد مثبتة ومستقرة على المدى الطويل',
            'تقليل المخاطر بطريقة علمية مدروسة',
            'شفافية كاملة في النتائج والأداء',
            'دعم فني على مدار الساعة',
            'تطوير مستمر للاستراتيجية',
            'مجتمع حصري من المستثمرين المحترفين'
        ],
        'statistics': [
            {'label': 'نسبة النجاح', 'value': '99%', 'icon': 'fas fa-chart-line'},
            {'label': 'العائد السنوي المتوسط', 'value': '1200%', 'icon': 'fas fa-percentage'},
            {'label': 'عدد العملاء', 'value': '1000+', 'icon': 'fas fa-users'},
            {'label': 'سنوات الخبرة', 'value': '5+', 'icon': 'fas fa-clock'}
        ]
    }
    return render(request, 'landing/service_details.html', context)


def telegram_details(request):
    """
    صفحة تفاصيل خدمة لايف على التليجرام
    """
    context = {
        'page_title': 'لايف على التليجرام - تفاصيل الخدمة',
        'service_name': 'لايف على التليجرام',
        'service_icon': 'fab fa-telegram',
        'description': 'تحليلات مباشرة وتوصيات فورية عبر قناة التليجرام مع متابعة لحظية للأسواق المالية.',
        'features': [
            'تحليلات مباشرة للأسواق العالمية',
            'توصيات دخول وخروج فورية',
            'تنبيهات السعر وإشارات التداول',
            'جلسات تعليمية مباشرة',
            'تفاعل مباشر مع الدكتور أحمد',
            'محتوى حصري يومي'
        ],
        'benefits': [
            'متابعة لحظية للفرص الاستثمارية',
            'تنفيذ سريع للصفقات المربحة',
            'تعلم مستمر من الخبرات العملية',
            'مجتمع نشط من المتداولين',
            'دعم فني مستمر',
            'أرشيف كامل للتحليلات السابقة'
        ],
        'statistics': [
            {'label': 'متابع نشط', 'value': '200+', 'icon': 'fab fa-telegram'},
            {'label': 'توصية يومية', 'value': '30+', 'icon': 'fas fa-bullhorn'},
            {'label': 'ساعات البث المباشر', 'value': '24', 'icon': 'fas fa-broadcast-tower'},
            {'label': 'دقة التوصيات', 'value': '97%', 'icon': 'fas fa-target'}
        ]
    }
    return render(request, 'landing/service_details.html', context)


def internal_deals_details(request):
    """
    صفحة تفاصيل الصفقات الداخلية
    """
    context = {
        'page_title': 'الصفقات الداخلية - تفاصيل الخدمة',
        'service_name': 'الصفقات الداخلية',
        'service_icon': 'fas fa-handshake',
        'description': 'فرص استثمارية حصرية وصفقات مدروسة بعناية لعملائنا المميزين مع عوائد استثنائية.',
        'features': [
            'صفقات حصرية غير متاحة للعامة',
            'تحليل معمق لكل فرصة استثمارية',
            'إدارة مخاطر متقدمة',
            'متابعة شخصية مع الدكتور أحمد',
            'تقارير أداء تفصيلية',
            'استشارة استثمارية شاملة'
        ],
        'benefits': [
            'عوائد مميزة تفوق السوق العام',
            'مخاطر محسوبة ومدروسة',
            'معلومات داخلية حصرية',
            'أولوية في الدخول والخروج',
            'دعم استثماري شخصي',
            'شبكة علاقات استثمارية قوية'
        ],
        'statistics': [
            {'label': 'العائد المتوسط يومياً', 'value': '5%', 'icon': 'fas fa-chart-bar'},
            {'label': 'الصفقات الناجحة', 'value': '97%', 'icon': 'fas fa-check-circle'},
            {'label': 'العملاء المميزين', 'value': '23+', 'icon': 'fas fa-crown'},
            {'label': 'الصفقات المكتملة', 'value': '289+', 'icon': 'fas fa-handshake'}
        ]
    }
    return render(request, 'landing/service_details.html', context)


def mt5_connection_details(request):
    """
    صفحة تفاصيل ربط حساب MT5
    """
    context = {
        'page_title': 'ربط حساب MT5 - تفاصيل الخدمة',
        'service_name': 'ربط حسابك بــ MT5',
        'service_icon': 'fas fa-link',
        'description': 'ربط سهل وآمن لحسابك مع منصة MetaTrader 5 لتنفيذ الصفقات بكفاءة عالية وأمان مطلق.',
        'features': [
            'ربط آمن 100% مع حماية البيانات',
            'تنفيذ تلقائي للإشارات',
            'مراقبة مستمرة للحساب',
            'تنفيذ سريع للصفقات',
            'إعدادات مخصصة لكل عميل',
            'دعم فني متخصص'
        ],
        'benefits': [
            'تنفيذ فوري للتوصيات',
            'تقليل الأخطاء البشرية',
            'تداول على مدار الساعة',
            'أمان عالي للحساب',
            'رصد مستمر للأداء',
            'مرونة في الإعدادات'
        ],
        'statistics': [
            {'label': 'الحسابات المربوطة', 'value': '11+', 'icon': 'fas fa-link'},
            {'label': 'سرعة التنفيذ', 'value': '0.1s', 'icon': 'fas fa-tachometer-alt'},
            {'label': 'مستوى الأمان', 'value': '100%', 'icon': 'fas fa-shield-alt'},
            {'label': 'معدل التوفر', 'value': '99.9%', 'icon': 'fas fa-server'}
        ]
    }
    return render(request, 'landing/service_details.html', context)
