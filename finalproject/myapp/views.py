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

    follow_list = []
    all_communities_list = []
    pending_friends_list = []
    friends_list = []
    current_user = "Guest"
    show_communities_tab = "True"
    
    if request.user.is_authenticated:

        all_communities_list = models.CommunityModel.objects.all()
        name = str(request.user.username)
        current_user = models.UserModel.objects.get(username=name)

        jsonDec = json.decoder.JSONDecoder()
        follow_list = jsonDec.decode(current_user.followed_communities)
        if len(follow_list) == 0:
            show_communities_tab = "False"
        pending_friends_list = jsonDec.decode(current_user.pending_friends_list)
        friends_list = jsonDec.decode(current_user.friends_list)

    context = {
        "title": "Final Project",
        "body":"Hello World",
        "all_communities_list": all_communities_list,
        "current_user": current_user,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "pending_friends_list": pending_friends_list,
        "friends_list": friends_list
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
            form.saveUser(request)
            return redirect("/login/")
    else:
        form = forms.RegistrationForm()
       #aboutForm = forms.UserAboutForm()

    context = {
        "title": "Registration Page",
         "form": form
    }
    return render(request,"registration/register.html", context=context)

def community_view(request, community_id):
    if request.method == "POST":
        return redirect("/")

    cur_community = models.CommunityModel.objects.get(community=community_id)
    about = cur_community.about
    show_communities_tab = "True"

    follow_list = []
    if request.user.is_authenticated:
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        jsonDec = json.decoder.JSONDecoder()
        follow_list = jsonDec.decode(current_user.followed_communities)
        if len(follow_list) == 0:
            show_communities_tab = "False"

    showFollow = False
    current_user = None
    if request.user.is_authenticated:
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        jsonDec = json.decoder.JSONDecoder()
        temp_list = []
        temp_list = jsonDec.decode(current_user.followed_communities)

        if str(community_id) not in temp_list:
            showFollow = True

    newComm = str(cur_community.community).replace(" ", "_")

    context = {
        "community_id": community_id,
        "slugName": newComm,
        "about": about,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "showFollow": showFollow,
        "current_user": current_user
    }

    return render(request,"community.html", context=context)

@login_required
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

@login_required
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

    #current_community_json_file = str(community_id) + ".json"

    with open("current_community.json", 'w') as jsonfile:
        json.dump(suggestion_list, jsonfile)

    link = "/community/" + str(community_id) + "/"
    return redirect(str(link))
    #return JsonResponse(suggestion_list)

@login_required
def suggestion_view(request, community_id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    follow_list = []
    name = request.user.username
    current_user = models.UserModel.objects.get(username=name)

    jsonDec = json.decoder.JSONDecoder()
    follow_list = jsonDec.decode(current_user.followed_communities)
    show_communities_tab = "True"

    if len(follow_list) == 0:
        show_communities_tab = "False"

    if request.method == "POST":
        form = forms.SuggestionForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, community_id)
            current_user.numPosts += 1
            link = "/cur_community/" + str(community_id) + "/"
            return redirect(str(link))
    else:
        form = forms.SuggestionForm()

    context = {
        "title": "Add Suggestion",
        "community_id": community_id,
        "form": form,
        "current_user": current_user,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab
    }
    return render(request,"suggestion.html", context=context)

@login_required
def comment_view(request, community_id, sugg_id):

    follow_list = []
    name = request.user.username
    current_user = models.UserModel.objects.get(username=name)

    jsonDec = json.decoder.JSONDecoder()
    follow_list = jsonDec.decode(current_user.followed_communities)

    show_communities_tab = "True"
    if len(follow_list) == 0:
        show_communities_tab = "False"

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, community_id, sugg_id)
            link = "/cur_community/" + str(community_id) + "/"
            return redirect(str(link))
    else:
        form = forms.CommentForm()

    context = {
        "title": "Comment",
        "community_id": community_id,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "sugg_id": sugg_id,
        "form": form
    }
    return render(request,"comment.html", context=context)

@login_required
def create_community_view(request):

    follow_list = []
    name = request.user.username
    current_user = models.UserModel.objects.get(username=name)

    jsonDec = json.decoder.JSONDecoder()
    follow_list = jsonDec.decode(current_user.followed_communities)

    show_communities_tab = "True"
    if len(follow_list) == 0:
        show_communities_tab = "False"

    if request.method == "POST":
        form = forms.CommunityForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)

            data = form.cleaned_data
            community_id = data['community_field']

            #Get the Follow List from the Current User
            jsonDec = json.decoder.JSONDecoder()
            temp_list = jsonDec.decode(current_user.followed_communities)

            #Add Current Community to user follow list once it is created
            if community_id not in temp_list:
                temp_list.append(str(community_id))
            current_user.followed_communities = json.dumps(temp_list)

            #Save the changes
            current_user.save()


            return redirect("/")
    else:
        form = forms.CommunityForm()


    context = {
        "title": "Create Communtiy",
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
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
    voteSum = []
    follow_list = []

    for p in posts:
        voteSum.append(p.vote)

    voteScore = sum(voteSum)

    current_profile = models.UserModel.objects.get(username=name)
    first_name = current_profile.first_name
    last_name = current_profile.last_name
    profile_username = current_profile.username
    profile_picture = current_profile.profile_picture
    numPosts = len(posts)
    areFriends = "False"
    pending = "False"

    jsonDec = json.decoder.JSONDecoder()
    friends_list = jsonDec.decode(current_profile.friends_list)

    numFriends = len(friends_list)
    show_communities_tab = "True"

    if request.user.is_authenticated:

        jsonDec = json.decoder.JSONDecoder()
        name = request.user.username
        my_profile = models.UserModel.objects.get(username=name)
        follow_list = jsonDec.decode(my_profile.followed_communities)

        numFollowed = len(follow_list)
        if numFollowed == 0:
            show_communities_tab = "False"

        if request.user.username in current_profile.friends_list:
            areFriends = "True"

        if request.user.username in current_profile.pending_friends_list:
            pending = "True"

    context = {
        "name": name,
        "first_name": first_name,
        "last_name": last_name,
        "current_user": current_profile,
        "profile_username": profile_username,
        "numPosts": numPosts,
        "numFollowed": numFollowed,
        "voteScore": voteScore,
        "numFriends": numFriends,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "profile_picture": profile_picture, 
        "areFriends": areFriends,
        "pending": pending
    }
    return render(request,"profile/profile.html", context=context)

@login_required
def update_profile_picture_view(request, name):

    follow_list = []
    current_user = models.UserModel.objects.get(username=name)

    jsonDec = json.decoder.JSONDecoder()
    follow_list = jsonDec.decode(current_user.followed_communities)

    if request.method == "POST":
        form = forms.UpdatePictureForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, name)
            link = "/profile/" + str(name) + "/"
            return redirect(str(link))
    else:
        form = forms.UpdatePictureForm()

    show_communities_tab = "True"
    if len(follow_list) == 0:
        show_communities_tab = "False"

    context = {
        "title": "Update Picture",
        "name": name,
        "current_user": current_user,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "form": form
    }
    return render(request,"profile/update_picture.html", context=context)

@login_required
def update_profile_about_view(request, name):

    follow_list = []
    current_user = models.UserModel.objects.get(username=name)

    jsonDec = json.decoder.JSONDecoder()
    follow_list = jsonDec.decode(current_user.followed_communities)

    if request.method == "POST":
        form = forms.UpdateAboutForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, name)
            link = "/profile/" + str(name) + "/"
            return redirect(str(link))
    else:
        form = forms.UpdateAboutForm()

    show_communities_tab = "True"
    if len(follow_list) == 0:
        show_communities_tab = "False"

    context = {
        "title": "Update About",
        "name": name,
        "current_user": current_user,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "form": form
    }
    return render(request,"profile/update_about.html", context=context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def chatIndex(request):
    return render(request, 'chat/chatIndex.html')

@login_required
def room(request, room_name):

    username = request.user.username
    messages = models.MessageModel.objects.filter(room=room_name)[0:25:-1]
    temp_room_name = str(room_name).replace("_", " ")

    cur_community = models.CommunityModel.objects.get(community=temp_room_name)
    room_name_back = str(cur_community.community).replace("_", " ")

    show_communities_tab = "True"
    if request.user.is_authenticated:
        follow_list = []
        name = request.user.username
        current_user = models.UserModel.objects.get(username=name)

        jsonDec = json.decoder.JSONDecoder()
        follow_list = jsonDec.decode(current_user.followed_communities)

        if len(follow_list) == 0:
            show_communities_tab = "False"

    context = {
        "room_name": room_name,
        "username": username,
        'messages': messages,
        "follow_list": follow_list,
        "show_communities_tab": show_communities_tab,
        "room_name_back": room_name_back
    }

    return render(request, 'chat/room.html', context=context)

def addFriend(request, name_to_follow, user_name):
    if request.method == "POST":
        return redirect("/")

    if request.user.is_authenticated:
        current_profile = models.UserModel.objects.get(username=name_to_follow)

        #Get the Friend List from the Current Profile
        jsonDec = json.decoder.JSONDecoder()
        temp_friends_list = jsonDec.decode(current_profile.friends_list)

        temp_pending_list = []
        temp_pending_list = jsonDec.decode(current_profile.pending_friends_list)
        #Add Pending Friend Request to user friend list
        if user_name not in temp_friends_list:
            if user_name not in temp_pending_list:
                temp_pending_list.append(str(user_name))

        current_profile.pending_friends_list = json.dumps(temp_pending_list)

        #Save the changes
        current_profile.save()

    link = "/profile/" + str(name_to_follow) + "/"

    return redirect(str(link))

def acceptFriendRequest(request, user_name_to_add, user_name):
    if request.method == "POST":
        return redirect("/")

    temp_friends_list = []
    temp_pending_list = []

    #Get CurrentUser
    if request.user.is_authenticated:
        current_profile = models.UserModel.objects.get(username=user_name)

        #Get the Follow List from the Current User
        jsonDec = json.decoder.JSONDecoder()
        temp_friends_list = jsonDec.decode(current_profile.friends_list)
        temp_pending_list = jsonDec.decode(current_profile.pending_friends_list)

        #User Accepting the Friend
        temp_friends_list.append(str(user_name_to_add))
        if user_name_to_add in temp_pending_list:
            temp_pending_list.remove(str(user_name_to_add))

        current_profile.friends_list = json.dumps(temp_friends_list)
        current_profile.pending_friends_list = json.dumps(temp_pending_list)

        #Save the changes
        current_profile.save()

        #User list who sent request gets updated
        other_profile = models.UserModel.objects.get(username=user_name_to_add)
        temp_friends_list = jsonDec.decode(other_profile.friends_list)
        temp_friends_list.append(str(user_name))

        other_profile.friends_list = json.dumps(temp_friends_list)

        #Save the changes
        other_profile.save()

    return redirect("/")

def declineFriendRequest(request, user_name_to_decline, user_name):
    if request.method == "POST":
        return redirect("/")

    temp_pending_list = []

    if request.user.is_authenticated:
        current_profile = models.UserModel.objects.get(username=user_name)

        #Get the Follow List from the Current User
        jsonDec = json.decoder.JSONDecoder()
        temp_pending_list = jsonDec.decode(current_profile.pending_friends_list)

        #Remove Pending Friend Request from list
        if user_name_to_decline in temp_pending_list:
            temp_pending_list.remove(str(user_name_to_decline))
        current_profile.pending_friends_list = json.dumps(temp_pending_list)

        #Save the changes
        current_profile.save()

    return redirect("/")

def removeFriend(request, name_to_remove, user_name):
    if request.method == "POST":
        return redirect("/")

    temp_friends_list = []
    temp_pending_list = []

    #Get Current User
    if request.user.is_authenticated:
        current_profile = models.UserModel.objects.get(username=name_to_remove)
        my_profile = models.UserModel.objects.get(username=user_name)
        jsonDec = json.decoder.JSONDecoder()

        #Get the Friend List from the Current Profile
        temp_friends_list = jsonDec.decode(current_profile.friends_list)

        #Remove Friend from your friends list
        if user_name in temp_friends_list:
            temp_friends_list.remove(str(user_name))
        current_profile.friends_list = json.dumps(temp_friends_list)

        #Save the changes to the Current Profile
        current_profile.save()

        #Get the Friend List from my Profile
        temp_friends_list = jsonDec.decode(my_profile.friends_list)

        #Remove Friend from your friends list
        if name_to_remove in temp_friends_list:
            temp_friends_list.remove(str(name_to_remove))
        my_profile.friends_list = json.dumps(temp_friends_list)

        #Save the changes to my Profile
        my_profile.save()

    link = "/profile/" + str(name_to_remove) + "/"

    return redirect(str(link))
