from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
from .models import *
from users.models import *
import jwt
from rest_framework.exceptions import AuthenticationFailed
# TODO: Remove @csrf_exempt after done debugging
# TODO: Add comment likes
# TODO: Add picture support
# TODO: Remove ability to add interactions on private posts (except for the blog user) Minor - add verification for every method (i.e., adding comments to make sure that the user has access to that post)
# TODO: Create a docker image for the database
# TODO: Insecure Deserialization - Exploitation of improperly deserialized objects to execute arbitrary code
# TODO: DOS - make a timeout per user requests
# TODO: check error handlers to not reveal secure info
# TODO: Secure session management and ensure proper timeout and invalidation mechanisms
# TODO: Check if request.user.id is received from jwt auth

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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not title or len(title) > 50:
            return JsonResponse({"error": "Title is required and cannot exceed 50 characters"}, status=400)
        
        if not content or len(content) > 2500:
            return JsonResponse({"error": "Content is required and cannot exceed 2500 characters"}, status=400)
        
        if not tags or len(tags) > 10:
            return JsonResponse({"error": "Tags are required and cannot have more than 10 entries"}, status=400)
        
        for tag in tags:
            if len(tag) > 30:
                return JsonResponse({"error": f"Tag '{tag}' exceeds the maximum length of 30 characters"}, status=400)

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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = get_object_or_404(User, id=user_id)

        blog_id = request.GET.get("blog_id")

        if not blog_id.isdigit():
            return JsonResponse({"error": "blog_id must be an integer"}, status=400)

        if not blog_id:
            return JsonResponse({"error": "blog_id not specified in query parameters"}, status=400)
        
        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        blog = get_object_or_404(Blogs, blog_id=blog_id)

        blog_data = {
            "blog_id": blog.blog_id,
            "title": blog.title,
            "content": blog.content,
            "tags": blog.tags,
            "access_level": blog.access_level,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
            "blog_creator": user.username,
        }

        if blog.access_level == 3 or blog.user_id == user.id:
            return JsonResponse({"blog": blog_data}, status=200)
        elif blog.access_level == 2:
            is_follower = Followers.objects.filter(follower_id=user.id, following_id=blog.user_id).exists()
            if is_follower:
                return JsonResponse({"blog": blog_data}, status=200)
            else:
                return JsonResponse({"error": "Not allowed"}, status=403)
        else:
            return JsonResponse({"error": "Not allowed"}, status=403)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_blogs(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        limit = 5
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        user = get_object_or_404(User, id=user_id)

        blogs_queryset = Blogs.objects.all()

        allowed_blogs_queryset = []
        for blog in blogs_queryset:
            access_level = blog.access_level
            blog_owner_id = blog.user_id

            if blog.user_id == user.id or access_level == 3:
                allowed_blogs_queryset.append(blog)
            elif access_level == 2:
                is_follower = Followers.objects.filter(follower_id=user.id, following_id=blog_owner_id).exists()
                if is_follower:
                    allowed_blogs_queryset.append(blog)

        if not allowed_blogs_queryset:
            return JsonResponse({"error": "No blogs found."}, status=403)

        paginator = Paginator(allowed_blogs_queryset, limit)
        current_page = paginator.page(page)

        blogs_data = []
        for blog in current_page:
            blog_creator = User.objects.get(id=blog.user_id)
            blog_data = {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "tags": blog.tags,
                "access_level": blog.access_level,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
                "blog_creator": blog_creator.username,
            }
            blogs_data.append(blog_data)

        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": len(allowed_blogs_queryset),
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": blogs_data, "pagination": pagination_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def get_user_blogs(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        searched_user_id = request.GET.get("searched_user_id")
        limit = 5
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not searched_user_id:
            return JsonResponse({"error": "searched_user_id is required"}, status=400)
        
        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid data type"}, status=400)
        
        try:
            searched_user_id = int(searched_user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid data type"}, status=400)

        user = get_object_or_404(User, id=user_id)
        searched_user = get_object_or_404(User, id=searched_user_id)

        blogs_queryset = Blogs.objects.filter(user_id=searched_user)

        allowed_blogs_queryset = []
        for blog in blogs_queryset:
            access_level = blog.access_level
            blog_owner_id = blog.user_id

            if blog.user_id == user.id or access_level == 3:
                allowed_blogs_queryset.append(blog)
            elif access_level == 2:
                is_follower = Followers.objects.filter(follower_id=user.id, following_id=blog_owner_id).exists()
                if is_follower:
                    allowed_blogs_queryset.append(blog)

        if not allowed_blogs_queryset:
            return JsonResponse({"error": "No blogs found."}, status=403)

        paginator = Paginator(allowed_blogs_queryset, limit)
        current_page = paginator.page(page)

        blogs_data = []
        for blog in current_page:
            blog_creator = User.objects.get(id=blog.user_id)
            blog_data = {
                "blog_id": blog.blog_id,
                "title": blog.title,
                "content": blog.content,
                "tags": blog.tags,
                "access_level": blog.access_level,
                "created_at": blog.created_at,
                "updated_at": blog.updated_at,
                "blog_creator": blog_creator.username,
            }
            blogs_data.append(blog_data)

        pagination_data = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_results": len(allowed_blogs_queryset),
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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not blog_id:
            return JsonResponse({"error": "blog_id is required"}, status=400)

        blog = get_object_or_404(Blogs, blog_id=blog_id)
        user = get_object_or_404(User, id=user_id)

        if blog.user_id != user.id:
            return JsonResponse({"error": "Unauthorized action"}, status=403)

        if title is not None:
            blog.title = title
        if content is not None:
            blog.content = content
        if tags is not None:
            blog.tags = tags
        if access_level is not None:
            blog.access_level = access_level

        # Remove likes, comments & bookmarks if a post is privated/followers-only
        if blog.access_level == 1:
            Interactions.objects.filter(blog=blog).exclude(user=blog.user).delete()
        elif blog.access_level == 2:
            followers = Followers.objects.filter(following=blog.user).values_list("follower_id", flat=True)
            Interactions.objects.filter(blog=blog ).exclude(Q(user=blog.user) | Q(user_id__in=followers)).delete()

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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)
        
        if not blog_id:
            return JsonResponse({"error": "blog_id is required"}, status=400)

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JsonResponse({"error": "Invalid blog_id"}, status=400)

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
        blog_id = data.get("blog_id")
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)
        
        if not content:
            return JsonResponse({"error": "Content is required"}, status=400)
        
        if not blog_id:
            return JsonResponse({"error": "Blog ID is required"}, status=400)

        blog = get_object_or_404(Blogs, pk=blog_id)
        user = get_object_or_404(User, pk=user_id)

        if blog.access_level == 1:
            return JsonResponse({"error": "Invalid action"}, status=403)
        elif blog.access_level == 2:
            is_follower = Followers.objects.filter(follower_id=user.id, following_id=blog.user_id).exists()
            if not is_follower:
                return JsonResponse({"error": "Invalid action"}, status=403)

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
        blog_id = request.GET.get("blog_id")
        limit = 10
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        blog = get_object_or_404(Blogs, blog_id=blog_id)

        comments_queryset = Comments.objects.filter(blog=blog)

        paginator = Paginator(comments_queryset, limit)
        current_page = paginator.page(page)

        for comment in current_page:
            comment_creator = User.objects.get(id=comment.user_id)
            comments_data = [
                {
                    "comment_id": comment.comment_id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at,
                    "user_id": comment.user_id,
                    "blog_id": comment.blog_id,
                    "comment_creator": comment_creator.username
                }
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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not comment_id:
            return JsonResponse({"error": "comment_id is required"}, status=400)
        
        if not isinstance(comment_id, int):
            return JsonResponse({"error": "Invalid comment_id format"}, status=400)

        comment = get_object_or_404(Comments, comment_id=comment_id)
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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")
        
        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not comment_id:
            return JsonResponse({"error": "comment_id is required"}, status=400)

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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not blog_id:
            return JsonResponse({"error": "Blog ID is required"}, status=400)

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
        blog_id = request.GET.get("blog_id")
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)
        
        if not blog_id:
            return JsonResponse({"error": "blog_id is required"}, status=400)

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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)
        
        if not blog_id:
            return JsonResponse({"error": "blog_id is required"}, status=400)

        try:
            blog_id = int(blog_id)
        except ValueError:
            return JsonResponse({"error": "Invalid blog_id"}, status=400)

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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not blog_id:
            return JsonResponse({"error": "Blog ID is required"}, status=400)

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
    # TODO: Maybe randomize how bookmarked posts are shown
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        limit = 5
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        bookmarked_queryset = Interactions.objects.filter(user_id=user_id, type=InteractionType.BOOKMARK.value)
        bookmarked_blog_ids = bookmarked_queryset.values_list("blog_id", flat=True)

        blogs_queryset = Blogs.objects.filter(blog_id__in=bookmarked_blog_ids)

        allowed_blogs_queryset = []
        for blog in blogs_queryset:
            access_level = blog.access_level
            blog_owner_id = blog.user_id

            if access_level == 3:
                allowed_blogs_queryset.append(blog)
            elif access_level == 2:
                is_follower = Followers.objects.filter(follower_id=user_id, following_id=blog_owner_id).exists()
                if is_follower:
                    allowed_blogs_queryset.append(blog)

        if not allowed_blogs_queryset:
            return JsonResponse({"error": "No blogs found."}, status=403)

        paginator = Paginator(allowed_blogs_queryset, limit)
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
            "total_results": len(allowed_blogs_queryset),
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
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)
        
        if not blog_id:
            return JsonResponse({"error": "blog_id is required"}, status=400)

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
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        tags = request.GET.getlist("tags")
        limit = 5
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not tags:
            return JsonResponse({"error": "tags are required"}, status=400)

        user = get_object_or_404(User, id=user_id)

        query = Q()
        for tag in tags:
            query |= Q(tags__contains=[tag])

        blogs_queryset = Blogs.objects.filter(query)

        allowed_blogs_queryset = []
        for blog in blogs_queryset:
            access_level = blog.access_level
            blog_owner_id = blog.user_id

            if access_level == 3 or blog.user_id == user.id:
                allowed_blogs_queryset.append(blog)
            elif access_level == 2:
                is_follower = Followers.objects.filter(follower_id=user.id, following_id=blog_owner_id).exists()
                if is_follower:
                    allowed_blogs_queryset.append(blog)

        if not allowed_blogs_queryset:
            return JsonResponse({"error": "No blogs found."}, status=403)

        paginator = Paginator(allowed_blogs_queryset, limit)
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
            "total_results": len(allowed_blogs_queryset),
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": blogs_data, "pagination": pagination_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def search_by_title(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        page = int(request.GET.get("page", 1))
        title = request.GET.get("title")
        limit = 5
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not title:
            return JsonResponse({"error": "title is required"}, status=400)

        user = get_object_or_404(User, id=user_id)

        blogs_queryset = Blogs.objects.filter(title__icontains=title)

        allowed_blogs_queryset = []
        for blog in blogs_queryset:
            access_level = blog.access_level
            blog_owner_id = blog.user_id

            if access_level == 3 or blog.user_id == user.id:
                allowed_blogs_queryset.append(blog)
            elif access_level == 2:
                is_follower = Followers.objects.filter(follower_id=user.id, following_id=blog_owner_id).exists()
                if is_follower:
                    allowed_blogs_queryset.append(blog)

        if not allowed_blogs_queryset:
            return JsonResponse({"error": "No blogs found."}, status=403)

        paginator = Paginator(allowed_blogs_queryset, limit)
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
            "total_results": len(allowed_blogs_queryset),
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
        }

        return JsonResponse({"blogs": blogs_data, "pagination": pagination_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def follow_user(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        following_id = data.get("following_id")
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            follower_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not follower_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

        if not following_id:
            return JsonResponse({"error": "Following ID is required"}, status=400)
        
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
        following_id = request.GET.get("following_id")
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            follower_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not follower_id:
            return JsonResponse({"error": "login required for this action"}, status=403)
        
        if not following_id:
            return JsonResponse({"error": "Following ID is required"}, status=400)
        
        follower = get_object_or_404(User, id=follower_id)
        following = get_object_or_404(User, id=following_id)

        follow = get_object_or_404(Followers, follower=follower, following=following)
        follow.delete()

        return JsonResponse({"message": "Follow deleted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_followers(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        following_id = request.GET.get("following_id")
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Token is missing"}, status=403)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        if not user_id:
            return JsonResponse({"error": "login required for this action"}, status=403)

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