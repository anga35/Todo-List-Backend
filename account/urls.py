from django.urls import path

from api import views


urlpatterns = [
    path('create/',views.CreateUserView.as_view(),name='create-user'),
    path('login/',views.LoginUserView.as_view(),name='login-user'),
    path('profile-pic/',views.UpdateProfilePictureView.as_view(),name='profile-pic'),
    path('get-token/',views.TokenGetView.as_view(),name='token-get'),
    path('get-user/',views.get_user_data,name='get-user'),
    path('reset-password-email/',views.GetResetPasswordURLView.as_view(),name='reset-password-email'),
    #/<uidb64>/<token>/
    path('reset-password/',views.ResetPassword.as_view(),name='reset-password',)


]