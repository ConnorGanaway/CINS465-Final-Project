import random
from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from slugify import slugify
import json

from . import models
from . import forms

# Create your views here.
def index(request):
    if request.method == "POST":
        redirect("/")

    community_list = []
    if request.user.is_authenticated:
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        #models.UserModel.objects.all(followed_communities)
        jsonDec = json.decoder.JSONDecoder()
        community_list = jsonDec.decode(current_user.followed_communities)

    context = {
        "title": "Final Project",
        "body":"Hello World",
        "community_list": community_list
    }
    return render(request,"index.html", context=context)

def logout_view(request):
    logout(request)
    return redirect("/login/")

def admin_view(request):
    return redirect("/admin/")

def delete_random(request):
    some_list = models.SuggestionModel.objects.all()
    if len(some_list) > 0:
        some_int = random.randrange(len(some_list))
        some_instance = some_list[some_int]
        some_instance.delete()
        return redirect("/")
    else:
        return redirect("/")

def register_view(request):
    username = None
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)

            #create user for UserModel
            form.saveUser(request)
            return redirect("/login/")
    else:
        form = forms.RegistrationForm()

    context = {
        "title": "Registration Page",
         "form": form
    }
    return render(request,"registration/register.html", context=context)

def community_view(request, community_id):
    if request.method == "POST":
        return redirect("/")

    community_list = []
    if request.user.is_authenticated:
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        #models.UserModel.objects.all(followed_communities)
        jsonDec = json.decoder.JSONDecoder()
        community_list = jsonDec.decode(current_user.followed_communities)

    showFollow = False
    current_user = None
    if request.user.is_authenticated:
        cur_community = models.CommunityModel.objects.get(community=community_id)
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)
        about = cur_community.about

        jsonDec = json.decoder.JSONDecoder()
        temp_list = []
        temp_list = jsonDec.decode(current_user.followed_communities)

        if str(community_id) not in temp_list:
            showFollow = True

    slugName = slugify(str(cur_community.community))

    context = {
        "community_id": community_id,
        "slugName": slugName,
        "about": about,
        "community_list": community_list,
        "showFollow": showFollow,
        "current_user": current_user
    }
    return render(request,"community.html", context=context)

def follow(request, community_id):
    if request.method == "POST":
        return redirect("/")

    #Get Current Community and User
    if request.user.is_authenticated:
        cur_community = models.CommunityModel.objects.get(community=community_id)
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        #Get the Follow List from the Current User
        jsonDec = json.decoder.JSONDecoder()
        temp_list = jsonDec.decode(current_user.followed_communities)

        #Add Current Community to user follow list
        if community_id not in temp_list:
            temp_list.append(str(community_id))
        current_user.followed_communities = json.dumps(temp_list)

        #Save the changes
        current_user.save()

    link = "/community/" + str(community_id) + "/"

    return redirect(str(link))

def unfollow(request, community_id):
    if request.method == "POST":
        return redirect("/")

    #Get Current Community and User
    if request.user.is_authenticated:
        cur_community = models.CommunityModel.objects.get(community=community_id)
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        #Get the Follow List from the Current User
        jsonDec = json.decoder.JSONDecoder()
        temp_list = jsonDec.decode(current_user.followed_communities)

        #Add Current Community to user follow list
        if community_id in temp_list:
            temp_list.remove(str(community_id))
        current_user.followed_communities = json.dumps(temp_list)

        #Save the changes
        current_user.save()

    link = "/community/" + str(community_id) + "/"

    return redirect(str(link))

def upvote(request, community_id, sugg_id):
    if request.method == "POST":
        return redirect("/")

    #Get Current Community and User
    if request.user.is_authenticated:
        cur_community = models.CommunityModel.objects.get(community=community_id)
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)
        current_post = models.SuggestionModel.objects.get(id=sugg_id)

        current_post.vote += 1
        current_post.save()

    link = "/community/" + str(community_id) + "/"

    return redirect(str(link))

def downvote(request, community_id, sugg_id):
    if request.method == "POST":
        return redirect("/")

    #Get Current Community and User
    if request.user.is_authenticated:
        cur_community = models.CommunityModel.objects.get(community=community_id)
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)
        current_post = models.SuggestionModel.objects.get(id=sugg_id)

        current_post.vote -= 1
        current_post.save()

    link = "/community/" + str(community_id) + "/"

    return redirect(str(link))


def cur_community_view(request, community_id):

    cur_community = models.CommunityModel.objects.get(community=community_id)
    suggestion_objects = models.SuggestionModel.objects.filter(community=cur_community).order_by("-published_on")
    suggestion_list = {}
    suggestion_list["suggestions"] = []
    for sugg in suggestion_objects:
        comment_objects = models.CommentModel.objects.filter(suggestion=sugg)
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        #community_object = models.CommunityModel.object.filter()
        temp_sugg["community"] = sugg.community.community
        temp_sugg["id"] = sugg.id
        temp_sugg["author"] = sugg.author.username
        temp_sugg["date"] = sugg.published_on.strftime("%Y-%m-%d")
        if sugg.image:
            temp_sugg["image"] = sugg.image.url
            temp_sugg["image_desc"] = sugg.image_description
        else:
            temp_sugg["image"] = ""
            temp_sugg["image_desc"] = ""
        temp_sugg["comments"] = []
        for comm in comment_objects:
            temp_comm = {}
            temp_comm["comment"] = comm.comment
            temp_comm["id"] = comm.id
            temp_comm["author"] = comm.author.username
            time_diff = datetime.now(timezone.utc) - comm.published_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_comm["date"] = "published " + str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s,60)[0]
                if time_diff_m < 60:
                    temp_comm["date"] = "published " + str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m,60)[0]
                    if time_diff_h < 24:
                        temp_comm["date"] = "published " + str(int(time_diff_h)) + " hours ago"
                    else:
                        temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S")
            temp_sugg["comments"] += [temp_comm]
        suggestion_list["suggestions"] += [temp_sugg]

    redirect("/login/")

    return JsonResponse(suggestion_list)

def suggestion_view(request, community_id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    community_list = []
    name = request.user.username
    current_user = models.UserModel.objects.get(username=name)

    #models.UserModel.objects.all(followed_communities)
    jsonDec = json.decoder.JSONDecoder()
    community_list = jsonDec.decode(current_user.followed_communities)

    if request.method == "POST":
        form = forms.SuggestionForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, community_id)
            current_user.numPosts += 1
            link = "/community/" + str(community_id) + "/"
            return redirect(str(link))
    else:
        form = forms.SuggestionForm()

    context = {
        "title": "Add Suggestion",
        "community_id": community_id,
        "form": form,
        "current_user": current_user,
        "community_list": community_list
    }
    return render(request,"suggestion.html", context=context)

@login_required
def comment_view(request, community_id, sugg_id):

    community_list = []
    name = request.user.username
    current_user = models.UserModel.objects.get(username=name)

    #models.UserModel.objects.all(followed_communities)
    jsonDec = json.decoder.JSONDecoder()
    community_list = jsonDec.decode(current_user.followed_communities)

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, community_id, sugg_id)
            link = "/community/" + str(community_id) + "/"
            return redirect(str(link))
    else:
        form = forms.CommentForm()

    context = {
        "title": "Comment",
        "community_id": community_id,
        "community_list": community_list,
        "sugg_id": sugg_id,
       "form": form
    }
    return render(request,"comment.html", context=context)

@login_required
def create_community_view(request):

    community_list = []
    name = request.user.username
    current_user = models.UserModel.objects.get(username=name)

    #models.UserModel.objects.all(followed_communities)
    jsonDec = json.decoder.JSONDecoder()
    community_list = jsonDec.decode(current_user.followed_communities)

    if request.method == "POST":
        form = forms.CommunityForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            return redirect("/")
    else:
        form = forms.CommunityForm()

    print("FORM CREATED")

    context = {
        "title": "Create Communtiy",
        "community_list": community_list,
        "form": form
    }
    return render(request,"create_community.html", context=context)

def suggestions_view(request):

    suggestion_objects = models.SuggestionModel.objects.all().order_by("-published_on")
    suggestion_list = {}
    suggestion_list["suggestions"] = []
    for sugg in suggestion_objects:
        comment_objects = models.CommentModel.objects.filter(suggestion=sugg)
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        #community_object = models.CommunityModel.object.filter()
        temp_sugg["community"] = sugg.community.community
        temp_sugg["id"] = sugg.id
        temp_sugg["vote"] = sugg.vote
        temp_sugg["author"] = sugg.author.username
        temp_sugg["date"] = sugg.published_on.strftime("%Y-%m-%d")
        if sugg.image:
            temp_sugg["image"] = sugg.image.url
            temp_sugg["image_desc"] = sugg.image_description
        else:
            temp_sugg["image"] = ""
            temp_sugg["image_desc"] = ""
        temp_sugg["comments"] = []
        for comm in comment_objects:
            temp_comm = {}
            temp_comm["comment"] = comm.comment
            temp_comm["id"] = comm.id
            temp_comm["author"] = comm.author.username
            time_diff = datetime.now(timezone.utc) - comm.published_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_comm["date"] = "published " + str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s,60)[0]
                if time_diff_m < 60:
                    temp_comm["date"] = "published " + str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m,60)[0]
                    if time_diff_h < 24:
                        temp_comm["date"] = "published " + str(int(time_diff_h)) + " hours ago"
                    else:
                        temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S")
            temp_sugg["comments"] += [temp_comm]
        suggestion_list["suggestions"] += [temp_sugg]

    return JsonResponse(suggestion_list)

def profile_view(request, name):
    if request.method == "POST":
        return redirect("/")

    posts = models.SuggestionModel.objects.filter(author__username=name)
    voteScore = None

    for p in posts:
        voteScore =+ p.vote

    if request.user.is_authenticated:
        community_list = []
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        #models.UserModel.objects.all(followed_communities)
        jsonDec = json.decoder.JSONDecoder()
        community_list = jsonDec.decode(current_user.followed_communities)

        numFollowed = len(community_list)

    context = {
        "name": name,
        "current_user": current_user,
        "numFollowed": numFollowed,
        "voteScore": voteScore,
        "community_list": community_list
    }
    return render(request,"profile.html", context=context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def chatIndex(request):
    return render(request, 'chat/chatIndex.html')

def room(request, room_name):

    if request.user.is_authenticated:
        community_list = []
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        #models.UserModel.objects.all(followed_communities)
        jsonDec = json.decoder.JSONDecoder()
        community_list = jsonDec.decode(current_user.followed_communities)

    context = {
        "room_name": room_name,
        "community_list": community_list
    }

    return render(request, 'chat/room.html', context=context)
