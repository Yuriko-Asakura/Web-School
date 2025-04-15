from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Courses)
admin.site.register(Predmet),
admin.site.register(Mod_Users),
admin.site.register(Roles),
admin.site.register(Topics),
admin.site.register(Lectures),
admin.site.register(Complexity),
admin.site.register(Levels),
admin.site.register(QuestionTypes),
admin.site.register(Tests),
admin.site.register(Questions),
admin.site.register(UserCourses),
admin.site.register(TopicTests)