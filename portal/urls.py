from django.urls import path

from .views import (
    admin_panel_view,
    create_request_view,
    dashboard_view,
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('requests/new/', create_request_view, name='create_request'),
    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('logout/', logout_view, name='logout'),
]
