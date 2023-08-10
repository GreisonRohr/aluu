from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Post, Rating
from django.db.models import Q

from django.db.models import Avg, Count, Sum

from django.shortcuts import get_object_or_404


import json


from .models import *


def index(request):

    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(
            followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(
            username=request.user.username).order_by("?")[:6]
    return render(request, "network/index.html", {
        "posts": posts,
        "suggestions": suggestions,
        "page": "all_posts",
        'profile': False
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Nome de usuário e/ou senha inválidos."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # Obtenha os valores dos campos do formulário
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        role = request.POST["role"]  # Novo campo "role"
        profile = request.FILES.get("profile")
        cover = request.FILES.get('cover')
        print(
            f"--------------------------Profile: {profile}----------------------------")
        cover = request.FILES.get('cover')
        print(
            f"--------------------------Cover: {cover}----------------------------")

        # Verifique se a senha corresponde à confirmação
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "As senhas devem corresponder."
            })

        # Tente criar um novo usuário com os valores fornecidos
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.role = role  # Salvar o valor selecionado no campo "role"

            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "profile_pic/no_pic.png"
            user.cover = cover
            user.save()
            Follower.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Nome de usuário já utilizado."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    user = User.objects.get(username=username)
    all_posts = Post.objects.filter(creater=user).order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    follower = False
    if request.user.is_authenticated:
        followings = Follower.objects.filter(
            followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(
            username=request.user.username).order_by("?")[:6]

        if request.user in Follower.objects.get(user=user).followers.all():
            follower = True

    follower_count = Follower.objects.get(user=user).followers.all().count()
    following_count = Follower.objects.filter(followers=user).count()

    return render(request, 'network/profile.html', {
        "username": user,
        "posts": posts,
        "posts_count": all_posts.count(),
        "suggestions": suggestions,
        "page": "profile",
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count
    })

##########################################


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        # Atualizar os dados do usuário com base nos valores enviados no formulário
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.save()
        # Redirecionar para a página de perfil ou outra página de sua escolha
        # Substitua 'perfil' pelo nome da sua rota de perfil de usuário
        return redirect('profile', username=user.username)
    else:

        user = request.user
        context = {
            'username': user.username,
            'email': user.email,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'role': user.role,
        }
    return render(request, 'network/edita.html', context)

    # Caso contrário, se for uma solicitação GET, renderize o formulário de edição de usuário


##########################################



def following(request):
    if request.user.is_authenticated:
        following_user = Follower.objects.filter(
            followers=request.user).values('user')
        all_posts = Post.objects.filter(
            creater__in=following_user).order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)
        followings = Follower.objects.filter(
            followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(
            username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "following"
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def saved(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(
            savers=request.user).order_by('-date_created')

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        followings = Follower.objects.filter(
            followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(
            username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "saved"
        })
    else:
        return HttpResponseRedirect(reverse('login'))

##################################################################


from django.db.models import Count, Avg

def ranking(request):
    top_rated_posts = Post.objects.annotate(
        avg_rating=Avg('ratings__rating_value')).order_by('-avg_rating')[:10]

    most_liked_posts = Post.objects.annotate(
        num_likes=Count('likers')).order_by('-num_likes')[:10]

    return render(request, "network/ranking.html", {
        "top_rated_posts": top_rated_posts,
        "most_liked_posts": most_liked_posts,
        "page": "ranking",
    })







@login_required
def search_posts(request):
    tags = request.GET.get('tags')  # Obtém o valor da pesquisa

    if tags:
        # Realiza a pesquisa de postagens com base nas tags
        posts = Post.objects.filter(tags__name__icontains=tags)
    else:
        # Retorna todas as postagens se não houver pesquisa
        posts = Post.objects.all()

    context = {
        'tags': tags,
        'posts': posts
    }

    return render(request, 'network/index.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        tag_name = request.POST.get('tag')  # Obtém o valor da tag relacionada

        try:
            post = Post.objects.create(
                creater=request.user, content_text=text, content_image=pic)  # Salva o novo post sem a tag relacionada

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)  # Associa a tag ao post

            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")


@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        img_chg = request.POST.get('img_change')
        # Obtém o valor atualizado da tag relacionada
        tag_name = request.POST.get('tag')

        try:
            post = Post.objects.get(id=post_id)

            post.content_text = text
            if img_chg != 'false':
                post.content_image = pic

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.clear()  # Remove todas as tags antigas do post
                post.tags.add(tag)  # Adiciona a nova tag ao post

            post.save()

            if post.content_text:
                post_text = post.content_text
            else:
                post_text = False
            if post.content_image:
                post_image = post.img_url()
            else:
                post_image = False

            return JsonResponse({
                "success": True,
                "text": post_text,
                "picture": post_image
            })
        except Exception as e:
            print('-----------------------------------------------')
            print(e)
            print('-----------------------------------------------')
            return JsonResponse({
                "success": False
            })
    else:
        return HttpResponse("Method must be 'POST'")


#################################################################################


@csrf_exempt
def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def save_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.savers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def unsave_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.savers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(
                f".....................Follower: {request.user}......................")
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(
                f".....................Unfollower: {request.user}......................")
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def comment(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            comment = data.get('comment_text')
            post = Post.objects.get(id=post_id)
            try:
                newcomment = Comment.objects.create(
                    post=post, commenter=request.user, comment_content=comment)
                post.comment_count += 1
                post.save()
                print(newcomment.serialize())
                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)

        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(id=post_id)
            if request.user == post.creater:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


def calculate_average_rating(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        # O post não existe, retorne um valor padrão ou levante uma exceção
        return None

    rating_stats = Rating.objects.filter(post=post).aggregate(
        average_rating=Avg('rating_value'),
        total_ratings=Count('id')
    )

    average_rating = rating_stats['average_rating'] or 0
    total_ratings = rating_stats['total_ratings']

    post.average_rating = average_rating
    post.total_ratings = total_ratings
    post.save()

    return average_rating


@csrf_exempt
def write_rating(request, post_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Você precisa estar logado para realizar uma avaliação.'})

    # Check if the user has already rated
    if Rating.objects.filter(user=request.user, post_id=post_id).exists():
        return JsonResponse({'success': False, 'message': 'Você já fez uma avaliação nesta postagem.'})

    try:
        data = json.loads(request.body)
        rating_value = data.get('rating_value')

        if not rating_value:
            return JsonResponse({'success': False, 'message': 'Valor de avaliação inválido.'})

        rating_value = float(rating_value)
        if rating_value < 0 or rating_value > 10:
            raise ValueError()

    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'message': 'Por favor, insira uma nota válida entre 0 e 10.'})

    # Save the rating in the database
    rating = Rating.objects.create(
        user=request.user, post_id=post_id, rating_value=float(rating_value))
    rating.save()
    # Calculate the average rating for the post
    average_rating = calculate_average_rating(post_id)
 # Pass the average rating as part of the context when rendering the page
    context = {
        'average_rating': average_rating
        # Rest of the context data...
    }
    # Return a success response with the updated data
    return JsonResponse({'success': True, 'message': 'Avaliação registrada com sucesso.', 'average_rating': average_rating, 'context': context})


def get_ratings(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ratings = Rating.objects.filter(post=post)

    data = {
        'success': True,
        'ratings': []
    }

    for rating in ratings:
        rating_data = {
            'id': rating.id,
            'value': rating.rating_value,  # Corrigido para acessar o campo rating_value
            'rater': {
                # Corrigido para acessar o usuário associado ao rating
                'username': rating.user.username,
                'first_name': rating.user.first_name,
                'last_name': rating.user.last_name,
                'profile_pic': rating.user.profile_pic.url if rating.user.profile_pic else ''
            }
        }
        data['ratings'].append(rating_data)

    return JsonResponse(data)
