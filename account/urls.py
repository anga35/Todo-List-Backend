from django.urls import path

from api.views import CreateUserView, LoginUserView, TokenGetView, UpdateProfilePictureView, get_user_data


urlpatterns = [
    path('create/',CreateUserView.as_view(),name='create-user'),
    path('login/',LoginUserView.as_view(),name='login-user'),
    path('profile-pic/',UpdateProfilePictureView.as_view(),name='profile-pic'),
    path('get-token/',TokenGetView.as_view(),name='token-get'),
    path('get-user/',get_user_data,name='get-user')


]