from . import views
from .views import RegisterAPI, UserList,LoginAPI
from django.urls import path
from knox.views import  LogoutView,LogoutAllView

urlpatterns = [
        path('', UserList.as_view()),
        path('api/register/', RegisterAPI.as_view(), name='register'),
        path('verify/', views.VerifyEmail.as_view(), name='verify'),
        path('api/login/', LoginAPI.as_view(), name='login'),
        path('api/logout/', LogoutView.as_view(), name='logout'),
]
