from django.urls import path
from . import views
from . import service_views

app_name = 'landing'

urlpatterns = [
    path('', views.index, name='index'),
    path('track-click/', views.track_click, name='track_click'),
    path('update-session/', views.update_session, name='update_session'),
    path('dashboard/', views.statistics_dashboard, name='dashboard'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('email-preview/', views.email_preview, name='email_preview'),
    
    # Service detail pages
    path('services/strategy/', service_views.strategy_details, name='strategy_details'),
    path('services/telegram/', service_views.telegram_details, name='telegram_details'),
    path('services/internal-deals/', service_views.internal_deals_details, name='internal_deals_details'),
    path('services/mt5-connection/', service_views.mt5_connection_details, name='mt5_connection_details'),
]
