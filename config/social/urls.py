from django.urls import path
from . import views

urlpatterns=[ 
    path("",views.PostView.as_view(),name="posts"),
    path("explore/",views.Explore.as_view(),name="explore"),
    path("create_thread",views.CreateThread.as_view(),name="create_thread"),
    path("search/",views.Search.as_view(),name="search"),
    path("search/<str:page>/ ",views.Search.as_view(),name="search"),
    path("profile/<str:pk>/",views.ProfileView.as_view(),name="profile"),
    path("update_profile/<str:pk>/",views.UpdateProfile.as_view(),name="update_profile"),
    path("post_detail/<str:pk>/",views.PostDetail.as_view(),name="post_detail"),
    path("update_post/<str:pk>/",views.UpdatePost.as_view(),name="update_post"),
    path("delete_post/<str:pk>/",views.DeletePost.as_view(),name="delete_post"),
    path("follow/<str:pk>/",views.Follow.as_view(),name="follow"),
    path("unfollow/<str:pk>/",views.UnFollow.as_view(),name="unfollow"),
    path("followers/<str:pk>/",views.Followers.as_view(),name="followers"),
    path("followings/<str:pk>/",views.Followings.as_view(),name="followings"),
    path("inbox/<str:pk>/",views.Inbox.as_view(),name="inbox"),
    path("thread/<str:pk>",views.ThreadView.as_view(),name="thread"),
    path("create_message/<str:pk>",views.CreateMessage.as_view(),name="create_message"),

    path("post/<str:post_pk>/update_comment/<str:pk>/",views.UpdateComment.as_view(),name="update_comment"),
    path("post/<str:post_pk>/delete_comment/<str:pk>/",views.DeleteComment.as_view(),name="delete_comment"),

    path("post/<str:post_pk>/like_comment/<str:pk>/",views.LikeComment.as_view(),name="like_comment"),
    path("post/<str:post_pk>/dislike_comment/<str:pk>/",views.DisLikeComment.as_view(),name="dislike_comment"),


    path("like/<str:pk>/",views.LikePost.as_view(),name="like_post"),
    path("dislike/<str:pk>/",views.DisLikePost.as_view(),name="dislike_post"),

    path("post/<str:post_pk>/replay_comment/<str:pk>/",views.ReplayComment.as_view(),name="replay_comment"),

    path("post/<str:post_pk>/notification/<str:notification_pk>/",views.PostNotification.as_view(),name="post_notification"),
    path("follow/<str:profile_pk>/notification/<str:notification_pk>/",views.FollowNotification.as_view(),name="follow_notification"),
    # path("thread/<str:thread_pk>/notification/<str:notification_pk>/",views.ThreadNotification.as_view(),name="thread_notification"),


]