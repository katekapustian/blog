from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import MyLogoutView, profile_view, update_profile

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<str:name>", views.post, name="post"),
    path("contacts", views.contact, name="contacts"),
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path('category/<str:c>', views.category, name="category"),
    path('search', views.search, name='search'),
    path('create', views.create, name='create'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/add_comment/<int:parent_id>/', views.add_comment, name='add_reply'),
    path('tag/<str:tag_name>/', views.tag_posts, name='tag_posts'),
    path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('subscribe', views.contact, name='subscribe'),
    path('login', LoginView.as_view(), name="blog_login"),
    path('logout', MyLogoutView.as_view(), name="blog_logout"),
    path('register/', views.register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
]
