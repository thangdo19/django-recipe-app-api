from django.urls import path

from user import views


# Register namespace
app_name = 'user'


# 'app_name' and 'name' is supported
# for 'reverse': 'user:create' when testing in request
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
