#Sources
#https://stackoverflow.com/questions/62704325/django-display-multiple-views-in-one-template
#https://stackoverflow.com/questions/59842406/how-to-pass-an-id-to-a-view-as-an-argument-in-django 
#https://stackoverflow.com/questions/23154525/django-generic-detail-view-must-be-called-with-either-an-object-pk-or-a-slug
#https://stackoverflow.com/questions/11494483/django-class-based-view-how-do-i-pass-additional-parameters-to-the-as-view-meth
#https://stackoverflow.com/questions/9561243/how-to-check-if-something-exists-in-a-postgresql-database-using-django
#https://stackoverflow.com/questions/9304908/how-can-i-filter-a-django-query-with-a-list-of-values
#http://www.intelligent-d2.com/python/access-url-parameters-django-cbvs/
#https://stackoverflow.com/questions/33785402/how-to-pass-multiple-url-parameters-in-django
#https://stackoverflow.com/questions/40187785/trying-to-filter-based-upon-a-value-in-another-table
#https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
#https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
#https://stackoverflow.com/questions/16849117/html-how-to-do-a-confirmation-popup-to-a-submit-button-and-then-send-the-reque

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import ExerciseEntry, Rewards, User, UserManager, Post, Followings, Comment, Location
from .forms import UpdateForm
from django.views import generic
from django.db.models import Q
from django.views.generic.edit import UpdateView
import requests
import json
from django.contrib import messages
import datetime 

# Create your views here.
from django.http import HttpResponse


def load(request):
    return render(request, 'exergam/feed.html')

def search(request):
    return render(request, 'exergam/search.html')

def location_option(request):
    if not Location.objects.filter(name="No Location", address="N/A").exists(): #Doesn't exist
        no_location = Location(name="No Location", address="N/A")
        no_location.save()
    no_location = Location.objects.get(name="No Location", address="N/A")
    return render(request, 'exergam/locationoption.html', {'no_location': no_location})

class HomeView(generic.DetailView): #How does the html know which user-> (PK)
    model = User 
    template_name = 'exergam/home.html'

    def get_queryset(self):
        return User.objects.all() 

    def get_object(self):
        return self.request.user

class ProfileView(generic.DetailView): 
    model = User 
    template_name = 'exergam/profile.html'
    context_object_name = 'profile'
        
    def get_queryset(self):
        return User.objects.all() # Thus, ProfileView will return object with id=pk from queryset

class MyLeaderboardView(generic.ListView):
    template_name = 'exergam/myleaderboard.html'
    context_object_name = 'ordered_user_list'

    def get_queryset(self):
        userid = self.request.user.id
        current_user = get_object_or_404(User, pk = userid)
        following = Followings.objects.filter(usr = current_user).values_list('following_usr')
        return User.objects.filter(Q(id__in = following) | Q(id=userid)).order_by('-total_points')

class LeaderboardView(generic.ListView):
    template_name = 'exergam/leaderboard.html'
    context_object_name = 'ordered_user_list'

    def get_queryset(self):
        return User.objects.order_by('-total_points')

class FeedView(generic.ListView):
    template_name = 'exergam/feed.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        userid = self.request.user.id
        current_user = get_object_or_404(User, pk = userid)
        following = Followings.objects.filter(usr = current_user).values_list('following_usr')
        posts = Post.objects.filter(Q(usr__in = following) | Q(usr=current_user)).order_by('-date')
        return posts

    def get_object(self):
        return self.request.user

class SearchView(generic.ListView):
    template_name = 'exergam/searchresults.html'
    context_object_name = 'searched_users_list'
    def get_queryset(self):
        to_search = self.request.GET['search_user'] #get the user's search
        print(type(to_search))
        print(to_search)
        possible_names = to_search.split() #Splits on space
        users = User.objects.filter(Q(email=to_search) | Q(usernm=to_search) | Q(first_nm__in=possible_names) | Q(last_nm__in=possible_names))
        return users

class LocationView(generic.ListView):
    template_name = 'exergam/selectlocation.html'
    context_object_name = 'locations_list'
    def get_queryset(self):
        search = self.request.GET["location"]
        search = search.replace(" ", "+")
        addresses = []
        if search != "":
            response = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + search + '&key=AIzaSyCP79RN8fzCpXK-wZLPhQKcqWq65WG8els')
            places = json.loads(response.text)
            for i in range(len(places['results'])):
                location_name = places['results'][i]['name']
                location_addr = places['results'][i]['formatted_address']
                if not Location.objects.filter(name=location_name, address=location_addr).exists():
                    new_location = Location(name=location_name, address=location_addr)
                    new_location.save()
                addresses.append(location_addr)
        return Location.objects.filter(address__in = addresses)

class UserUpdateView(UpdateView):
    model = User
    fields = ['usernm','first_nm','last_nm','picture']
    template_name = 'exergam/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'post'
    
    def get_object(self,queryset=None):
        return self.request.user

    def form_valid(self, form):
        user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect(reverse('exergam:profile', args=(user_id,)))
    

def add_entries(request): # creating an exercise entry for the user
    user_id = request.user.id
    current_user = get_object_or_404(User, pk=user_id)
    # current_user = get_object_or_404(User, pk = request.user.id)

    now = timezone.now()
    #Need to handle invalid input
    exercise_type = request.POST["exercise_type_dropdown"]
    description = request.POST["description"]
    exercise_date = request.POST["exercise_date"]
    exercise_duration = request.POST["exercise_duration"]

    if description == "" or exercise_date == "" or exercise_duration == "":
        messages.error(request, "Looks like you left something blank. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))

    # These 3 elif statements handle invalid dates
    if int(exercise_date[0:4]) > int(now.year):
        messages.error(request, "Looks like you have entered an invalid date. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))
    elif int(exercise_date[0:4]) == int(now.year) and int(exercise_date[5:7]) > int(now.month):
        messages.error(request, "Looks like you have entered an invalid date. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))
    elif int(exercise_date[0:4]) == int(now.year) and int(exercise_date[5:7]) == int(now.month) and int(exercise_date[8:10]) > int(now.day):
        messages.error(request, "Looks like you have entered an invalid date. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))

    else:
        if int(exercise_duration) > 1440 :
            messages.error(request, "You are inputting too many minutes at once. Try again!")
            return HttpResponseRedirect(reverse('exergam:feed'))

        entry = ExerciseEntry(exercise_type=exercise_type,
                              description=description,
                              exercise_date=exercise_date,
                              exercise_duration=exercise_duration,
                              usr=current_user)

        entry.save()
        if not Rewards.objects.filter(reward_type=exercise_type, usr=current_user).exists():
            badge = Rewards(reward_type=exercise_type, usr=current_user)
            badge.save()
        # calculate total points
        if exercise_type == "Walking":
            user_points = current_user.total_points + float(entry.exercise_duration) * 100 * 0.75
        else:
            user_points = current_user.total_points + float(entry.exercise_duration) * 100
        current_user.total_points = user_points
        current_user.rank = update_rank(user_points)
        current_user.save()
        return HttpResponseRedirect(reverse('exergam:profile', args=[user_id]))#, args=(user_id,)))

def newentry(request):  # Basic page to put a new entry in
    return render(request, 'exergam/upload.html')


def add_post(request):
    user_id = request.user.id
    current_user = get_object_or_404(User, pk=user_id)
    now = timezone.now()
   
    text = request.POST.get("post_text", "")
    #date = request.POST.get("post_date", "")
    location = request.POST.get("location", "")

    if text == "" or location == "":
        messages.error(request, "You left something blank. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))

    else:
        post = Post(text=text,
                    date=timezone.now(),#-datetime.timedelta(hours=4), #convert to EST
                    location=location,
                    usr=current_user)
        post.save()
        return HttpResponseRedirect(reverse('exergam:profile', args=[user_id]))#, args=(user_id,)))

def newpost(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'exergam/post.html', {'location': location})

def follow(request, follow_id):
    user_id = request.user.id
    current_user = get_object_or_404(User, pk = user_id)
    user_to_follow = get_object_or_404(User, pk = follow_id)
    if not Followings.objects.filter(usr=current_user, following_usr=user_to_follow).exists():
        following = Followings(usr=current_user, following_usr=user_to_follow)
        following.save()
    return HttpResponseRedirect(reverse('exergam:profile', args=(user_to_follow.id,)))


def unfollow(request, unfollow_id):
    user_id = request.user.id
    current_user = get_object_or_404(User, pk = user_id)
    user_to_unfollow = get_object_or_404(User, pk = unfollow_id)
    if Followings.objects.filter(usr=current_user, following_usr=user_to_unfollow).exists():
        Followings.objects.filter(usr=current_user, following_usr=user_to_unfollow).delete()
        return HttpResponseRedirect(reverse('exergam:profile', args=(user_to_unfollow.id,)))
    else:
        messages.error(request, "You don't follow this user.")
        return HttpResponseRedirect(reverse('exergam:profile', args=(user_to_unfollow.id,)))


# Comment on someone else's post. Can only be done on the Feed section, redirects to feed after comment
def comment_on_other(request, post_id):
    #Not used?
    user_id = request.user.id
    current_user = get_object_or_404(User, pk=user_id)
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment(text=request.POST.get("comment_text", ""),
                      date=timezone.now(),#-datetime.timedelta(hours=4), #convert to EST,
                      author=current_user,
                      assc_post=post)

    if comment.text == "":
        messages.error(request, "You can't post a blank comment. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))

    comment.save()
    return HttpResponseRedirect(reverse('exergam:feed'))#, args=(user_id,)))


# Comment on your own post. Needs separate because your own posts do not show on post feed, only your profile. So redirect to profile
def comment_on_own(request, post_id):
    #print("called")
    user_id = request.user.id
    current_user = get_object_or_404(User, pk=user_id)
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment(text=request.POST.get("comment_text", ""),
                      date=timezone.now(),#-datetime.timedelta(hours=4), #convert to EST,
                      author=current_user,
                      assc_post=post)

    if comment.text == "":
        messages.error(request, "You can't post a blank comment. Try again!")
        return HttpResponseRedirect(reverse('exergam:feed'))

    comment.save()
    return HttpResponseRedirect(reverse('exergam:feed'))#, args=(user_id,)))
 
def update_rank(points):
    if points < 365000:
        return "Unranked"
    elif 365000 <= points < 547500:
        return "Bronze"
    elif 547500 <= points < 1095000:
        return "Silver"
    elif 1095000 <= points < 1642500:
        return "Gold"
    elif 1642500 <= points < 2190000:
        return "Platinum"
    else:
        return "Diamond"
