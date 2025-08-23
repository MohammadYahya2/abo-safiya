from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from datetime import datetime, timedelta
from .models import Visitor, ClickEvent, PageView, DailyStats
import json


def statistics_dashboard(request):
    """
    عرض لوحة الإحصائيات المفصلة
    """
    # إحصائيات عامة
    total_visitors = Visitor.objects.count()
    total_page_views = PageView.objects.count()
    total_clicks = ClickEvent.objects.count()
    
    # إحصائيات اليوم
    today = timezone.now().date()
    today_visitors = Visitor.objects.filter(first_visit__date=today).count()
    today_page_views = PageView.objects.filter(timestamp__date=today).count()
    today_clicks = ClickEvent.objects.filter(timestamp__date=today).count()
    
    # إحصائيات آخر 7 أيام
    last_7_days = timezone.now() - timedelta(days=7)
    weekly_visitors = Visitor.objects.filter(first_visit__gte=last_7_days).count()
    
    # إحصائيات آخر 30 يوم
    last_30_days = timezone.now() - timedelta(days=30)
    monthly_visitors = Visitor.objects.filter(first_visit__gte=last_30_days).count()
    
    # إحصائيات الأجهزة
    device_stats = Visitor.objects.values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # أكثر الصفحات زيارة
    popular_pages = PageView.objects.values('page_url').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # أكثر الأزرار نقراً
    popular_buttons = ClickEvent.objects.values('element_clicked').annotate(
        clicks=Count('id')
    ).order_by('-clicks')[:10]
    
    # إحصائيات يومية لآخر 30 يوم (للرسم البياني)
    daily_stats = []
    for i in range(30):
        date = today - timedelta(days=i)
        visitors_count = Visitor.objects.filter(first_visit__date=date).count()
        page_views_count = PageView.objects.filter(timestamp__date=date).count()
        daily_stats.append({
            'date': date.strftime('%Y-%m-%d'),
            'visitors': visitors_count,
            'page_views': page_views_count
        })
    
    daily_stats.reverse()  # ترتيب تصاعدي
    
    # معدل التحويل (النقرات مقسومة على الزوار)
    conversion_rate = (total_clicks / total_visitors * 100) if total_visitors > 0 else 0
    
    # متوسط مدة الجلسة
    avg_session = Visitor.objects.aggregate(
        avg_duration=Avg('session_duration')
    )['avg_duration'] or 0
    
    # الزوار العائدون
    returning_visitors = Visitor.objects.filter(visit_count__gt=1).count()
    returning_rate = (returning_visitors / total_visitors * 100) if total_visitors > 0 else 0
    
    # حساب النسبة المئوية للنمو (مقارنة مع أمس)
    yesterday = today - timedelta(days=1)
    yesterday_visitors = Visitor.objects.filter(first_visit__date=yesterday).count()
    growth_rate = 0
    if yesterday_visitors > 0:
        growth_rate = ((today_visitors - yesterday_visitors) / yesterday_visitors) * 100
    
    context = {
        'title': 'إحصائيات الموقع المفصلة',
        'total_visitors': total_visitors,
        'total_page_views': total_page_views,
        'total_clicks': total_clicks,
        'today_visitors': today_visitors,
        'today_page_views': today_page_views,
        'today_clicks': today_clicks,
        'weekly_visitors': weekly_visitors,
        'monthly_visitors': monthly_visitors,
        'device_stats': device_stats,
        'popular_pages': popular_pages,
        'popular_buttons': popular_buttons,
        'daily_stats_json': json.dumps(daily_stats),
        'conversion_rate': round(conversion_rate, 2),
        'avg_session': round(avg_session / 60, 2) if avg_session else 0,  # بالدقائق
        'returning_rate': round(returning_rate, 2),
        'returning_visitors': returning_visitors,
        'growth_rate': round(growth_rate, 1),
    }
    
    return render(request, 'dashboard.html', context)
