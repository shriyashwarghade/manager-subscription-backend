from django.urls import path

from . import views

urlpatterns = [
    path('api/products', views.products),
    path('api/create-user', views.create_user),
    path('api/login-request', views.login_request),
    path('api/logout-request', views.logout_request),
    path('api/user-info', views.user_info),
    path('api/subscription', views.subscription)
]
