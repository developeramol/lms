from django.urls import path
from webapp import views

urlpatterns = [
    path('input_animation', views.input_animation, name='input_animation'),
    path('home_requests', views.home_requests, name='home_requests'),
    path('webhook_example/',views.webhook_example, name='webhook_example'),

    path('login', views.login_form, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('notifications/', views.notifications, name='notifications'),
    path('', views.super_admin_dashboard),

    path('lead_source_create_form/', views.lead_source_create_form, name='lead_source_create_form'),
    path('lead_source_view/', views.lead_source_view, name='lead_source_view'),
    path('lead_source_update_form/<int:id>/', views.lead_source_update_form, name='lead_source_update_form'),
    path('lead_source_delete/<int:id>/', views.lead_source_delete, name='lead_source_delete'),

    path('lead_status_create_form/', views.lead_status_create_form, name='lead_status_create_form'),
    path('lead_status_view/', views.lead_status_view, name='lead_status_view'),
    path('change_status/', views.change_status, name='change_status'),
    path('lead_status_update_form/<int:id>/', views.lead_status_update_form, name='lead_status_update_form'),

    path('admin_user_create_form/', views.admin_user_create_form, name='admin_user_create_form'),
    # path('admin_user_update_form/<int:id>/', views.admin_user_update_form, name='admin_user_update_form'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('admin_client_user_view/', views.admin_client_user_view, name='admin_client_user_view'),
    path('admin_user_data/', views.admin_user_data, name='admin_user_data'),
    path('delete_admin_data/<int:id>/', views.delete_admin_data, name='delete_admin_data'),
    path('change_password/', views.change_password, name='change_password'),

    path('client_user_create_form/', views.client_user_create_form, name='client_user_create_form'),

    path('lead_view/', views.lead_view, name='lead_view'),
    # path('lead_status_update/<int:lead_id>/', views.Lead_Status_Update.as_view(), name='lead_status_update'),
    path('lead_create_form/', views.lead_create_form, name='lead_create_form'),
    path('lead_update_form/<int:id>/', views.lead_update_form, name='lead_update_form'),
    path('lead_history_eye_data/<int:id>/', views.lead_history_eye_data, name='lead_history_eye_data'),
    path('lead_history_form/<int:id>/', views.lead_history_form_view, name='lead_history_form'),
    # path('lead_history_form_inside_eye/<int:id>/', views.lead_history_form_view_inside_eye, name='lead_history_form_inside_eye'),
    path('lead_delete/<int:id>/', views.lead_delete, name='lead_delete'),
    path('export/csv/', views.export_lead_excel_sheet_csv, name='export_lead_excel_sheet_csv'),

    path('customer_form/', views.customer_form, name='customer_form'),
    path('customer_data/', views.customer_data, name='customer_data'),
    path('customer_eye_data/<int:id>/', views.customer_eye_data, name='customer_eye_data'),
    path('delete_customer_data/<int:id>/', views.delete_customer_data, name='delete_customer_data'),
    path('customer_update_form/<int:id>/', views.customer_update_form, name='customer_update_form'),
]
