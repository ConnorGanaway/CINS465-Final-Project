import random
from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

# Create your views here.
def index(request):
    if request.method == "POST":
        redirect("/")

    community_objects = models.CommunityModel.objects.all()
    community_list = []
    for c in community_objects:
        community_list += [c.community]

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
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
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

    context = {
        "name": "CURRENT COMMUNITY NAME - FIX THIS",
        "community_id": community_id
    }
    return render(request,"community.html", context=context)

def suggestion_view(request, community_id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, community_id)
            return redirect("/community/{{ community_id }}/")
    else:
        form = forms.SuggestionForm()

    context = {
        "title": "Add Suggestion",
        "community_id": community_id,
       "form": form
    }
    return render(request,"suggestion.html", context=context)

@login_required
def comment_view(request, community_id, sugg_id):
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, community_id, sugg_id)
            return redirect("/")
    else:
        form = forms.CommentForm()

    context = {
        "title": "Comment",
        "community_id": community_id,
        "sugg_id": sugg_id,
       "form": form
    }
    return render(request,"comment.html", context=context)

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
