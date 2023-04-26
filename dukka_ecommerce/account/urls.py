
from django.urls import path
from . import views


urlpatterns = [
    path('auth/new/account', views.RegisterUsersView.as_view(), name='register_user-account'),

    path('auth/accounts', views.AllUserAccountsView.as_view(), name='get_user_accounts'),

    path('auth/account', views.UserAccountView.as_view(), name="get_user_account")
]