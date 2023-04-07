from django.urls import path, include

from telegram_reg.views import HomeView, RegisterView, AccountView, save_user

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('register/', RegisterView.as_view(), name='register'),
    path('save-user/', save_user, name='save_new_user'),

]
