from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register-user/', views.regiser_user, name='register-user'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('users-list/', views.UsersListView.as_view(), name='users-list'),
    path('user-delete/<slug:username>/', views.UserDeleteView.as_view(), name='user-delete'),
    path('profile/<slug:username>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<slug:username>/update', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<slug:username>/reviews/', views.UserReviewsView.as_view(), name='user_reviews'),
    path('profile/<slug:username>/create-review/', views.ReviewCreateView.as_view(), name='create-review'),

]

