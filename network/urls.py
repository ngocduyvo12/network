
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #api routes
    path("compose", views.compose, name="compose"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following/<int:id>", views.following, name="following"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("feed", views.feed, name = "feed"),
    path("update/<int:id>", views.update, name="update"),
    path("like/<int:id>", views.like, name="like"),
    
]
