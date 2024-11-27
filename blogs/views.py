from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
from .models import *
from users.models import *
# TODO: Remove @csrf_exempt after done debugging
# TODO: change query & json to be more consistent with URI
# TODO: Add friends, followers (& respective tables)
# TODO: Check if blog should be displayed the user (access_level) ---- after adding followers table (public is already done)
# TODO: Change how user_id is handled
# TODO: Add comment likes
# TODO: get username instead of user_id

# TODO: Add picture support
@csrf_exempt
def create_blog(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")
        tags = data.get("tags")
        access_level = data.get("access_level", AccessLevel.PUBLIC.value)
        # TODO: change the way user_id is handled
        user_id = data.get("user_id")
        # user_id = request.user.user_id

        if title:
            blog = Blogs.objects.create(
                title=title,
                content=content,
                tags=tags,
                access_level=access_level,
                user_id=user_id
            )
            return JsonResponse({"message": "Blog created successfully", "blog_id": blog.blog_id})
        else:
            return JsonResponse({"error": "Required fields not filled in"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_blog(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        blog_id = request.GET.get("blog_id")
        if blog_id:
            blog = Blogs.objects.get(blog_id=blog_id)

            if blog:
                blog_data = {
                    "blog_id": blog.blog_id,
                    "title": blog.title,
                    "content": blog.content,
                    "tags": blog.tags,
                    "access_level": blog.access_level,
                    "created_at": blog.created_at,
                    "updated_at": blog.updated_at,
                }
                
                if blog.access_level == 4:
                    return JsonResponse({"blog": blog_data}, status=200)
                else:
                    return JsonResponse({"error": "Not allowed"}, status=403)
            else:
                return JsonResponse({"error": "Blog not found"}, status=404)
        else:
            return JsonResponse({"error": "blog_id not specified in query parameters"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_blogs(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        # TODO: Change how limits are handled
        limit = 5

        blogs_queryset = Blogs.objects.all()

        paginator = Paginator(blogs_queryset, limit)
        current_page = paginator.page(page)

        blogs_data = [
            {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "tags": blog.tags,
                "access_level": blog.access_level,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
            }
            for blog in current_page
        ]

        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": blogs_data, "pagination": pagination_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_blog(request):
    if request.method != 'PUT':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")
        tags = data.get("tags")
        access_level = data.get("access_level")
        blog_id = data.get("blog_id")

        if not blog_id:
            return JsonResponse({"error": "blog_id is required"}, status=400)

        blog = get_object_or_404(Blogs, blog_id=blog_id)

        if title is not None:
            blog.title = title
        if content is not None:
            blog.content = content
        if tags is not None:
            blog.tags = tags
        if access_level is not None:
            blog.access_level = access_level

        blog.save()

        blog_data = {
            "blog_id": blog.blog_id,
            "title": blog.title,
            "content": blog.content,
            "tags": blog.tags,
            "access_level": blog.access_level,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
        }

        return JsonResponse({"message": "Blog updated successfully", "blog": blog_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def delete_blog(request):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        blog_id = request.GET.get("blog_id")
        user_id = request.GET.get("user_id")
        
        if not blog_id or not user_id:
            return JsonResponse({"error": "blog_id & user_id are required"}, status=400)

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JsonResponse({"error": "Invalid blog_id"}, status=400)

        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid user_id"}, status=400)

        blog = get_object_or_404(Blogs, blog_id=blog_id)

        if blog.user_id != user_id:
            return JsonResponse({"error": "Unauthorized action"}, status=403)

        blog.delete()

        return JsonResponse({"message": "Blog deleted successfully", "blog_id": blog_id}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def add_comment(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        content = data.get("content")
        #TODO: Might need to change how ids are handled
        blog_id = data.get("blog_id")
        user_id = data.get("user_id")

        if not content:
            return JsonResponse({"error": "Content is required"}, status=400)
        if not blog_id:
            return JsonResponse({"error": "Blog ID is required"}, status=400)
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)

        blog = get_object_or_404(Blogs, pk=blog_id)
        user = get_object_or_404(User, pk=user_id)

        interaction = Interactions.objects.create(
            user=user,
            blog=blog,
            type=InteractionType.COMMENT.value,
        )

        comment = Comments.objects.create(
            content=content,
            blog=blog,
            interaction=interaction,
            user=user
        )


        return JsonResponse({"message": "Comment created successfully", "comment_id": comment.comment_id})
        
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_comments(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        limit = 10

        comments_queryset = Comments.objects.all()

        paginator = Paginator(comments_queryset, limit)
        current_page = paginator.page(page)

        comments_data = [
            {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "user_id": comment.user_id,
                "blog_id": comment.blog_id,
            }
            for comment in current_page
        ]

        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"comments": comments_data, "pagination": pagination_data}, status=200)
    
    except ValueError:
        return JsonResponse({"error": "Invalid query parameters"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def edit_comment(request):
    if request.method != 'PUT':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        content = data.get("content")
        comment_id = data.get("comment_id")
        user_id = data.get("user_id")

        if not comment_id:
            return JsonResponse({"error": "comment_id is required"}, status=400)
        
        if not isinstance(comment_id, int):
            return JsonResponse({"error": "Invalid comment_id format"}, status=400)

        comment = get_object_or_404(Comments, comment_id=comment_id)
        # TODO: Remind frontend to send the id with the json
        if user_id != comment.user_id:
            return JsonResponse({"error": "Unauthorized action"}, status=403)

        if content is not None:
            if content.strip() == "":
                return JsonResponse({"error": "Content cannot be empty"}, status=400)
            comment.content = content


        comment.save()

        comment_data = {
            "comment_id": comment.comment_id,
            "content": comment.content,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "blog_id": comment.blog_id,
            "user_id": comment.user_id,
        }

        return JsonResponse({"message": "Comment updated successfully", "comment": comment_data}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def delete_comment(request):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        comment_id = request.GET.get("comment_id")
        user_id = request.GET.get("user_id")
        
        if not comment_id or not user_id:
            return JsonResponse({"error": "comment_id & user_id are required"}, status=400)

        try:
            comment_id = int(comment_id)
        except ValueError:
            return JsonResponse({"error": "Invalid comment_id"}, status=400)

        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid user_id"}, status=400)

        comment = get_object_or_404(Comments, comment_id=comment_id, user_id=user_id)

        if comment.user_id != user_id:
            return JsonResponse({"error": "Unauthorized action"}, status=403)
        
        comment.delete()
        Interactions.objects.filter(interaction_id=comment.interaction_id).delete()


        return JsonResponse({"message": "Comment deleted successfully", "comment_id": comment_id}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def add_like(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        blog_id = data.get("blog_id")
        user_id = data.get("user_id")

        if not blog_id:
            return JsonResponse({"error": "Blog ID is required"}, status=400)
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)

        blog = get_object_or_404(Blogs, pk=blog_id)
        user = get_object_or_404(User, pk=user_id)

        if Interactions.objects.filter(user_id=user_id, blog_id=blog_id, type=InteractionType.LIKE.value).exists():
            return JsonResponse({"error": "User already liked this blog"}, status=400)


        interaction = Interactions.objects.create(
            user=user,
            blog=blog,
            type=InteractionType.LIKE.value,
        )

        return JsonResponse({"message": "Like added successfully", "interaction_id": interaction.interaction_id})
        
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_likes(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        blog_id = data.get("blog_id")

        likes = Interactions.objects.filter(blog_id=blog_id, type=InteractionType.LIKE.value).count()

        return JsonResponse({"like_count": likes}, status=200)
    
    except ValueError:
        return JsonResponse({"error": "Invalid query parameters"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def delete_like(request):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        blog_id = request.GET.get("blog_id")
        user_id = request.GET.get("user_id")
        
        if not blog_id or not user_id:
            return JsonResponse({"error": "blog_id & user_id are required"}, status=400)

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JsonResponse({"error": "Invalid blog_id"}, status=400)

        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid user_id"}, status=400)

        like = get_object_or_404(Interactions, blog_id=blog_id, user_id=user_id, type=InteractionType.LIKE.value)

        if like.user_id != user_id:
            return JsonResponse({"error": "Unauthorized action"}, status=403)
        
        like.delete()

        return JsonResponse({"message": "Like deleted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def add_bookmark(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        blog_id = data.get("blog_id")
        user_id = data.get("user_id")

        if not blog_id:
            return JsonResponse({"error": "Blog ID is required"}, status=400)
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)

        blog = get_object_or_404(Blogs, pk=blog_id)
        user = get_object_or_404(User, pk=user_id)

        if Interactions.objects.filter(user_id=user_id, blog_id=blog_id, type=InteractionType.BOOKMARK.value).exists():
            return JsonResponse({"error": "User already bookmarked this blog"}, status=400)


        interaction = Interactions.objects.create(
            user=user,
            blog=blog,
            type=InteractionType.BOOKMARK.value,
        )

        return JsonResponse({"message": "Bookmark added successfully", "interaction_id": interaction.interaction_id})
        
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_bookmark_posts(request):
    # TODO: Only display blogs that the user is allowed to see (access_level) + if a bookmarked post was privated, we need to remove the bookmarks once the user privates it.
    # TODO: Maybe change how bookmarked posts are shown, as they're currently shown in the order they were added to the table (randomize?)
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        # TODO: Change how limits are handled
        limit = 5
        # TODO: Change how user_id is handled
        data = json.loads(request.body)
        user_id = data.get("user_id")
        bookmarked_queryset = Interactions.objects.filter(user_id=user_id, type=InteractionType.BOOKMARK.value)
        bookmarked_blog_ids = bookmarked_queryset.values_list('blog_id', flat=True)
        blogs_queryset = Blogs.objects.filter(blog_id__in=bookmarked_blog_ids)

        paginator = Paginator(blogs_queryset, limit)
        current_page = paginator.page(page)

        blogs_data = [
            {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "tags": blog.tags,
                "access_level": blog.access_level,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
            }
            for blog in current_page
        ]

        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": blogs_data, "pagination": pagination_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def remove_bookmark(request):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        blog_id = request.GET.get("blog_id")
        # TODO: Change this lmao
        user_id = request.GET.get("user_id")
        
        if not blog_id or not user_id:
            return JsonResponse({"error": "blog_id & user_id are required"}, status=400)

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JsonResponse({"error": "Invalid blog_id"}, status=400)

        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid user_id"}, status=400)

        bookmark = get_object_or_404(Interactions, blog_id=blog_id, user_id=user_id, type=InteractionType.BOOKMARK.value)

        if bookmark.user_id != user_id:
            return JsonResponse({"error": "Unauthorized action"}, status=403)
        
        bookmark.delete()

        return JsonResponse({"message": "Bookmark deleted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def search_by_tag(request):
    # TODO: Only display blogs that the user is allowed to see (access_level)
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        # TODO: Change how limits are handled
        limit = 5
        data = json.loads(request.body)
        tags = data.get("tags", [])

        query = Q()
        for tag in tags:
            query |= Q(tags__contains=[tag])

        blogs_queryset = Blogs.objects.filter(query)

        paginator = Paginator(blogs_queryset, limit)
        current_page = paginator.page(page)

        blogs_data = [
            {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "tags": blog.tags,
                "access_level": blog.access_level,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
            }
            for blog in current_page
        ]

        allowed_blogs_data = [
            blog_data for blog_data in blogs_data if blog_data["access_level"] == 3
        ]

        if not allowed_blogs_data:
            return JsonResponse({"error": "No blogs found."}, status=403)


        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": allowed_blogs_data, "pagination": pagination_data}, status=200)


    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def search_by_title(request):
    # TODO: Only display blogs that the user is allowed to see (access_level)
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        title = request.GET.get("title")
        # TODO: Change how limits are handled
        limit = 5

        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        blogs_queryset = Blogs.objects.filter(title__icontains=title)

        paginator = Paginator(blogs_queryset, limit)
        current_page = paginator.page(page)

        blogs_data = [
            {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "tags": blog.tags,
                "access_level": blog.access_level,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
            }
            for blog in current_page
        ]

        allowed_blogs_data = [
            blog_data for blog_data in blogs_data if blog_data["access_level"] == 3
        ]

        if not allowed_blogs_data:
            return JsonResponse({"error": "No blogs found."}, status=403)

        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": allowed_blogs_data, "pagination": pagination_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def follow_user(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        follower_id = data.get("follower_id")
        following_id = data.get("following_id")
        #TODO: check if follower id = user_id

        if not follower_id or not following_id:
            return JsonResponse({"error": "Follower/Following ID are required"}, status=400)
        
        if follower_id == following_id:
            return JsonResponse({"error": "Users cannot follow themselves"}, status=400)
        
        follower = get_object_or_404(User, id=follower_id)
        following = get_object_or_404(User, id=following_id)

        if Followers.objects.filter(follower_id=follower_id, following_id=following_id).exists():
            return JsonResponse({"error": "User is already following this user"}, status=400)

        follow = Followers.objects.create(
            follower=follower,
            following=following,
        )

        return JsonResponse({"message": "Follow added successfully", "action_id": follow.action_id}, status=201)
        
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def unfollow_user(request):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        follower_id = request.GET.get("follower_id")
        following_id = request.GET.get("following_id")
        
        if not follower_id or not following_id:
            return JsonResponse({"error": "Follower/Following ID are required"}, status=400)
        
        follower = get_object_or_404(User, id=follower_id)
        following = get_object_or_404(User, id=following_id)

        follower = get_object_or_404(Followers, follower=follower, following=following)
        #TODO: check if follower id = user_id
        follower.delete()

        return JsonResponse({"message": "Follow deleted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_followers(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        following_id = request.GET.get("following_id")

        following = get_object_or_404(User, id=following_id)

        followers = Followers.objects.filter(following=following).count()

        return JsonResponse({"followers count": followers}, status=200)
    
    except ValueError:
        return JsonResponse({"error": "Invalid query parameters"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_replies():
    pass