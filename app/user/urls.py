from django.urls import path

from user import views


app_name = 'user'


# 'app_name' and 'name' is supported for 'reverse': 'user:create'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
