from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Rewards, ExerciseEntry
# Register your models here.

#https://stackoverflow.com/questions/25468676/django-sites-model-what-is-and-why-is-site-id-1

class EntryInLine(admin.StackedInline):
    model = ExerciseEntry
    extra = 1

class RewardsInLine(admin.StackedInline):
    model = Rewards
    extra = 1

class ExergamUserAdmin(UserAdmin):
    list_display = ('email','total_points','is_superuser')
    search_fields = ('email',)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = () 
    ordering = ('email','total_points','is_superuser')
    inlines = [EntryInLine, RewardsInLine]

admin.site.register(User, ExergamUserAdmin)