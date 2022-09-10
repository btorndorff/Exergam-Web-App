from django.test import TestCase, Client, override_settings
from .models import User, UserManager, Followings, Rewards, Post, ExerciseEntry, Location
from .views import FeedView, ProfileView, HomeView, UserUpdateView, SearchView, LocationView, LeaderboardView
import datetime
from django.utils import timezone
from django.urls import reverse, resolve, path
from django import forms

# Create your tests here.
# class DummyTestCase(TestCase):
#     #def test_account_configured(self):
#     def setUp(self):
#         x = 1
    
#     def test_dummy_test_case(self):
#         self.assertEqual(1, 1)
#         #self.assertTrue('user' in INSTALLED_APPS)
#         #self.assertTrue('user.User' == AUTH_USER_MODEL)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestViews(TestCase):
    def setUp(self):
        #self.email = "testing123@example.com"
        self.client = Client()
        self.user = User.objects.create_superuser(email = "testing123456@gmail.com", password="testpassword").save()
        
        self.new_post_url = reverse('exergam:new_post', args=[1])
        self.new_profile_url = reverse('exergam:profile', args=[1])
        self.load_url = reverse('exergam:feed')
        self.feed_url = reverse('exergam:profile', args=[1])
        self.locationOne = Post.objects.create(text = 1, date = timezone.now())
        self.client2 = Client()
        self.user2 = User.objects.create_superuser(email = "jjnivar@gmail.com", password="testpassword2").save()
        
    def test_loggedInUsers(self):
        login = self.client.login(email = "testing123456@gmail.com", password="testpassword")

        #response = self.client.get(self.feed_url)
        self.assertTrue(login)
        #print(str(response.context))
        
    def test_loggedInUsers2(self):
        login2 = self.client2.login(email = "jjnivar@gmail.com", password="testpassword2")
        self.assertTrue(login2)

    def test_nav_bar2(self):
        response = self.client.get(self.feed_url)
        self.assertIn('testing123456@gmail.com', str(response.context['profile']))
        #print(str(response.context['profile']))

    def test_homeView_statusCode(self):
        self.homeView_url = reverse('exergam:home')
        response = self.client.get(self.homeView_url)
        self.assertEquals(response.status_code, 200)
        
        
    def test_Location_post(self):
        #self.user = User.objects.create_user(email = "testing123456@gmail.com")
        #locationNumOne = Location.objects.create(name="Paris", address="England")
        response = self.client.get(self.new_profile_url)
        newPost = Post.objects.create(
            text = "worked out today",
            date = timezone.now(),
            location = "Paris")
        self.assertEquals(response.status_code, 200) #get it to run 200

    def test_newpost(self):
        newPost = Post.objects.create(
            text = "worked out today",
            date = timezone.now(),
            location = "Paris")
        #print(str(newPost))
        self.assertEquals(newPost.text, "worked out today")
        self.assertEquals(newPost.location, "Paris")

    def test_load_GET(self):
        response = self.client.get(self.load_url)
        self.assertEquals(response.status_code, 404)
        #self.assertTemplateUsed(response, 'exergam/feed.html')
        
    def test_noNewPosts_GET(self):
        response = self.client.get(self.new_post_url)
        self.assertEquals(response.status_code, 404) #should return 404
        
        
    def test_no_added_post_POST(self):
        self.user = User.objects.create_user(email = "testing123@gmail.com")
        posts = Post.objects.create(
            text = "testing posts",
            date = timezone.now(),
            location = "",
            usr = self.user)
            
        response = self.client.post(self.new_post_url, {
            'text' : posts.text,
            'date' : posts.date,
            'location' : posts.location
        })
        
        self.assertEquals(response.status_code, 404)
    
#Testing basic user instantiations 
class UserTest(TestCase):
    def setUp(self):
        self.email = "testinguser@testbase.com"
        self.password = "hi"
        
        self.test_user = User.objects.create_user(email = self.email)

    def test_create_user(self):
        self.assertIsInstance(self.test_user, User)
        
    def test_user_is_active(self):
        self.assertTrue(self.test_user.is_active)
        
    def test_user_is_staff(self):
        self.assertFalse(self.test_user.is_staff)

    def test_user_is_superuser(self):
        self.assertFalse(self.test_user.is_superuser)
    
    def test_default_total_points(self):
        self.assertEquals(self.test_user.total_points, 0)
        
    def test_default_username(self):
        self.assertEquals(self.test_user.usernm, 'exergam_user')
        
#Testing badge types
class myRewardsTest(TestCase):
    def setUp(self):
        Rewards.objects.create(reward_type="Basketball Badge")
        
    def test_default_badge_type(self):
        badge = Rewards.objects.get()
        self.assertEquals(badge.reward_type, 'Basketball Badge')

#Testing whether users count for "Following" goes up when they follow somebody new
class FollowingsTest(TestCase):
    def setUp(self):
        self.email1 = "testinguser1@testbase.com"  
        self.test_user1 = User.objects.create_user(email = self.email1)
        self.email2 = "testinguser2@testbase.com"  
        self.test_user2 = User.objects.create_user(email = self.email2)
        self.email3 = "testinguser3@testbase.com"  
        self.test_user3 = User.objects.create_user(email = self.email3)


    def test_followings_simple(self):
        following1 = Followings(usr = self.test_user1, following_usr=self.test_user2).save()
        following2 = Followings(usr = self.test_user1, following_usr=self.test_user3).save()
        followings = self.test_user1.following.all()

        #print(type(followings))
        self.assertEquals(2, len(followings))
        
#Testing no exercise logged in terms of time
class myExerciseEntryTest(TestCase):
    def setUp(self):
        time = timezone.now()
        ExerciseEntry.objects.create(exercise_date = time)
        
    def test_exercise_entry(self):
        exercise = ExerciseEntry.objects.get()
        self.assertEquals(exercise.exercise_duration, 0)

#Testing posts with no unique identifiers
class myPostsTest(TestCase):
    def setUp(self):
        time = timezone.now()
        Post.objects.create(date = time)

    def test_default_postsView(self):
        posts = Post.objects.get()
        self.assertEquals(posts.text, '')
    
    def test_default_postsView2(self):
        posts2 = Post.objects.get()
        self.assertEquals(posts2.location, '')
        
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class HomePageTests(TestCase):

#"""Test whether our blog entries show up on the homepage"""

    def setUp2(self):
        self.user = User.objects.create(email = "test1232@river.com")

    def test_one_entry(self):
        ExerciseEntry.objects.create(exercise_type = 'Basketball',
                                    description = 'test description',
                                    exercise_date = timezone.now(),
                                    exercise_duration = 25)
        response = self.client.get('/')
        self.assertNotContains(response, 'test description')
        self.assertNotContains(response, 'Basketball')
        self.assertNotContains(response, 'Exercise History')
