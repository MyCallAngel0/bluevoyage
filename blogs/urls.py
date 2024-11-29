from django.urls import path
from .views import *
# TODO: add a bucket for images, store the id in the .env, make use of the email in .env 

urlpatterns = [
    path('create_blog', create_blog),
    # Single blog (individual view)
    path('get_blog', get_blog),
    path('get_blogs', get_blogs),
    path('get_user_blogs', get_user_blogs),
    path('update_blog', update_blog),
    path('delete_blog', delete_blog),
    path('add_comment', add_comment),
    path('get_comments', get_comments),
    path('edit_comment', edit_comment),
    path('delete_comment', delete_comment),
    path('add_like', add_like),
    path('get_likes', get_likes),
    path('delete_like', delete_like),
    path('add_bookmark', add_bookmark),
    path('get_bookmark_posts', get_bookmark_posts),
    path('remove_bookmark', remove_bookmark),
    path('search_by_tag', search_by_tag),
    path('search_by_title', search_by_title),
    path('follow_user', follow_user),
    path('unfollow_user', unfollow_user),
    path('get_followers', get_followers),
    # Getting comments left on a comment
    path('get_replies', get_replies),
]