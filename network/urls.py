
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("n/login", views.login_view, name="login"),
    path("n/logout", views.logout_view, name="logout"),
    path("n/register", views.register, name="register"),
    path("n/edita", views.edit_profile, name="edit_profile"),
    path("n/search", views.search_posts, name="search_posts"),
    path("<str:username>", views.profile, name='profile'),
    path("n/following", views.following, name='following'),
    path("n/saved", views.saved, name="saved"),
    path("n/createpost", views.create_post, name="createpost"),
    path("n/post/<int:id>/like", views.like_post, name="likepost"),
    path("n/post/<int:id>/unlike", views.unlike_post, name="unlikepost"),
    path("n/post/<int:id>/save", views.save_post, name="savepost"),
    path("n/post/<int:id>/unsave", views.unsave_post, name="unsavepost"),
    path("n/post/<int:post_id>/comments", views.comment, name="comments"),
    path("n/post/<int:post_id>/delete", views.delete_post, name="deletepost"),
    path("<str:username>/follow", views.follow, name="followuser"),
    path("<str:username>/unfollow", views.unfollow, name="unfollowuser"),
    path("n/post/<int:post_id>/edit", views.edit_post, name="editpost"),
    path("n/post/<int:post_id>/write_rating",
         views.write_rating, name="writerating"),
    path("n/post/<int:post_id>/get_ratings",
         views.get_ratings, name="getratings"),
    path("n/ranking", views.ranking, name="ranking"),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
