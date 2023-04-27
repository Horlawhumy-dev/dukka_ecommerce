
from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('new/account', views.RegisterUsersView.as_view(), name='register_user_account'),

    path('accounts', views.AllUserAccountsView.as_view(), name='get_user_accounts'),

    path('account', views.UserAccountView.as_view(), name="get_user_account")
]