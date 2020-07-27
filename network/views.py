import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    #get posts from data base
    posts = Post.objects.all()
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #check ownership
    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
    })

# def get_posts(request, page):

def feed(request):
    #filter through the current user's following list:
    user = User.objects.get(id = request.user.id)
    following = user.following.all()
    id_list = []
    for element in following:
        id_list.append(element.id)
    posts = Post.objects.filter(poster__in = id_list)    

    return render(request, 'network/feed.html', {
        "posts": posts,
    })

def profile(request, id):
    #get all post from the current profile
    posts = Post.objects.filter(
        poster = id
    )
    
    #sort the posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()
    #check if the the current user is the owner of the profile:
    if request.user.id == id:
        owner = True
    else:
        owner = False

    #calculate like counts


    if (len(posts) == 0):
        return render(request, 'network/profile.html', {
            "empty": True,
            "owner":owner
        })
    else:
        return render(request, 'network/profile.html', {
            "posts": posts,
            "id": id,
            "owner": owner
        })

@csrf_exempt
def update(request, id):
    post = Post.objects.get(
        id = id
    )
    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)    

def like(request, id):
    #get the post that was clicked on:
    post = Post.objects.get(
        id = id
    )
    user = User.objects.get(
        id = request.user.id
    )

    #check to see if the user has already liked the post:
    check = post.likes.filter(id = request.user.id)

    #if check is not empty then user has already liked it. So unlike instead:
    if check:
        post.likes.remove(user)
    else:
        post.likes.add(user)

    #get the number of people that likes the post:
    count = post.likes.count()
    return JsonResponse({"count": count})

#function to follow a user
@login_required
def following(request, id):
    #get the currently logged in user's profile:
    currentUser = User.objects.get(id = request.user.id)
    #get the current page's profile:
    profileUser = User.objects.get(id = id)

    #check if the current logged in user is already following this user:
    #get the current logged in user following list:
    followingCheck = currentUser.following.filter(id = id)

    if currentUser == profileUser:
        return JsonResponse({"message": "You cannot follow yourself"}, status = 400)
    #if followingCheck have something in it then we know the user is already following
    elif followingCheck:
        #return code 1 user is trying to follow someone they already followed
        return JsonResponse({"code": "1"})
    else:
        currentUser.following.add(profileUser)
        #render the current page again
    #if everything went well return code 2
    return JsonResponse({"code": "2"})


#function to unfollow a user
@login_required
def unfollow(request, id):
    #get the currently logged in user's profile:
    currentUser = User.objects.get(id = request.user.id)
    #get the current page's profile:
    profileUser = User.objects.get(id = id)

    #check if the current logged in user is already following this user:
    #get the current logged in user following list:
    followingCheck = currentUser.following.filter(id = id)

    if followingCheck:
        #return code 3 for successfully unfollowed a user
        currentUser.following.remove(profileUser)
        return JsonResponse({"code": "3"})
    else:
        #if is not currently following this user then return code 4 error
        return JsonResponse({"code": "4"})



@csrf_exempt
@login_required
def compose(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # get data from request
    data = json.loads(request.body)
    body = data.get("body", "")

    
    post = Post(
        user = request.user,
        poster=request.user,
        content=body,
    )
    post.save()


    return JsonResponse({"message": "Post created successfully.", "body": body,}, status=201)


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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
