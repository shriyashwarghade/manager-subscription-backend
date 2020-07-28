from django.urls import path

from . import views

urlpatterns = [
    path('api/products', views.Products.as_view()),
    path('api/create-user', views.CreateUser.as_view()),
    path('api/login-request', views.LoginRequest.as_view()),
    path('api/logout-request', views.LogoutRequest.as_view()),
    path('api/user-info', views.UserInfo.as_view()),
    path('api/subscription', views.Subscription.as_view())
]
