#Sources
#https://docs.djangoproject.com/en/3.1/ref/models/fields/
#https://pyphilly.org/know-thy-user-custom-user-models-django-allauth/
#https://learndjango.com/tutorials/django-custom-user-model
#https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
#https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#specifying-custom-user-model
#https://www.youtube.com/watch?v=SFarxlTzVX4&ab_channel=CodingWithMitch
#https://www.geeksforgeeks.org/creating-custom-user-model-using-abstractuser-in-django_restframework/
#https://stackoverflow.com/questions/9800490/django-onetoonefield-in-which-model-should-i-put-it
#https://stackoverflow.com/questions/38117069/django-charfield-suitable-for-a-primary-key
#https://stackoverflow.com/questions/16925129/generate-unique-id-in-django-from-a-model-field
#https://docs.djangoproject.com/en/3.1/topics/db/examples/one_to_one/
#https://stackoverflow.com/questions/18941720/auto-creating-related-objects-on-model-creation-in-django
#https://stackoverflow.com/questions/1652550/can-django-automatically-create-a-related-one-to-one-model
#https://stackoverflow.com/questions/5608001/create-onetoone-instance-on-model-creation
#https://stackoverflow.com/questions/26685065/django-create-instance-of-model-from-another-models-save-method
#https://stackoverflow.com/questions/52196365/django-automatically-create-a-model-instance-when-another-model-instance-is-cr/52196467
#https://docs.djangoproject.com/en/2.1/ref/signals/#django.db.models.signals.post_save
#https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
#https://depositphotos.com/113097904/stock-illustration-animal-avatars-flat-vector-icons.html for the animal icons

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique = True, blank = False)
    usernm = models.CharField(
        max_length = 40,
        default = "exergam_user"
        )
    first_nm = models.CharField(
        max_length = 40,
        default = "Exergam"
        )
    last_nm = models.CharField(
        max_length = 40,
        default = "User"
        )
    USERNAME_FIELD = 'email' #Something wrong here
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    total_points = models.IntegerField(default = 0)

    rank = models.CharField(
        max_length = 30,
        default = 'Unranked'
    )
    PICTURE_CHOICES = [
        ('../images/default.jpeg', 'Default'),
        ('../images/1.jpg', '1'),
        ('../images/2.jpg', '2'),
        ('../images/3.jpg', '3'),
        ('../images/4.jpg', '4'),
        ('../images/5.jpg', '5'),
        ('../images/6.jpg', '6'),
        ('../images/7.jpg', '7'),
        ('../images/8.jpg', '8'),
        ('../images/9.jpg', '9'),
        ('../images/10.jpg', '10'),
        ('../images/12.jpg', '12'),
        ('../images/13.jpg', '13'),
        ('../images/14.jpg', '14'),
        ('../images/15.jpg', '15'),
        ('../images/16.jpg', '16'),
        ('../images/17.jpg', '17'),
        ('../images/18.jpg', '18'),
        ('../images/19.jpg', '19'),
        ('../images/20.jpg', '20'),
    ]

    picture = models.ImageField(choices=PICTURE_CHOICES, default = "../images/default.jpeg")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def unranked(self): 
        return self.rank == 'Unranked' 
    
    def bronze(self): 
        return self.rank == 'Bronze' 
    
    def silver(self): 
        return self.rank == 'Silver' 
    
    def gold(self): 
        return self.rank == 'Gold' 
    
    def platinum(self): 
        return self.rank == 'Platinum' 
    
    def diamond(self): 
        return self.rank == 'Diamond'

class ExerciseEntry(models.Model):
    EXERCISE_CHOICES = [
        ('Basketball', 'Basketball'),
        ('Baseball', 'Baseball'),
        ('Climbing', 'Climbing'),
        ('Football', 'Football'),
        ('Frisbee', 'Frisbee'),
        ('Soccer', 'Soccer'),
        ('Spikeball', 'Spikeball'),
        ('Swimming', 'Swimming'),
        ('Tennis', 'Tennis'),
        ('Track + Field', 'Track + Field'),
        ('Volleyball', 'Volleyball'),
        ('Walking', 'Walking'),
        ('Weightlifting', 'Weightlifting'),
        ('Yoga', 'Yoga'),
        ('Cardio', 'Cardio'), #Broad categories from here down to cover the rest
        ('Strength', 'Strength')
    ]
    exercise_type = models.CharField( 
        max_length = 30, 
        choices = EXERCISE_CHOICES, 
        )
    description = models.CharField(
        max_length = 300,
        )
    exercise_date = models.DateTimeField('Date Exercised')
    exercise_duration = models.IntegerField(
        default = 0
    )
    # many-to-one relationship with User
    usr = models.ForeignKey(User, on_delete = models.CASCADE, null=True) 

class Rewards(models.Model):
    # reward_type is just the type of badge, the only valid types are the exercise types e.g. basketball badge
    reward_type = models.CharField(
        max_length = 30,
    )
    
    # many-to-one relationships to User -> each User has associated badges
    usr = models.ForeignKey(User, on_delete = models.CASCADE, null=True) 

class Post(models.Model):
    text = models.TextField()
    date = models.DateTimeField()
    location = models.TextField(default="")
    usr = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    assc_post = models.ForeignKey(Post, on_delete = models.CASCADE, null=True) #associated post

class Followings(models.Model):
    usr = models.ForeignKey(User,on_delete = models.CASCADE, related_name="following", null=True)
    following_usr = models.ForeignKey(User, on_delete = models.CASCADE, related_name="followers", null=True)


class Location(models.Model):
    name = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.name + " (" + self.address + ")"

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Rewards.objects.create(usr=instance)
