from django.urls import path
from . import views
from .views import UpdatePostView


urlpatterns = [
    #     blogs
    path("", views.blogs, name="blogs"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("blog/<int:id>", views.post_by_id, name="add_blogs"),
    path("edit_blog_post/<int:pk>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("delete_blog_post/<int:id>/", views.delete_post, name="delete_blog_post"),
    path("search/", views.search, name="search"),

    #     profile
    path("profile/", views.profile, name="profile"),


    #    user authentication
    path("register/", views.register, name="register"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
]