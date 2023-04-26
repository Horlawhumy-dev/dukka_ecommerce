
from django.urls import path
from . import views


urlpatterns = [
    path('new/account', views.RegisterUsersView.as_view(), name='register_user-account'),

    path('accounts', views.AllUserAccountsView.as_view(), name='get_user_accounts'),

    path('account', views.UserAccountView.as_view(), name="get_user_account")
]