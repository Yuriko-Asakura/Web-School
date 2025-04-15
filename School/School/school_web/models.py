from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required  # Add this
from django.db import models

class Roles(models.Model):
    ID_Role = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Mod_Users(models.Model):
    ID_User = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=100, blank=False, null=False)
    Email = models.EmailField(unique=True, blank=False, null=False)
    Password = models.CharField(max_length=255, blank=False, null=False)
    image = models.BinaryField(blank=True, null=True)
    Number = models.IntegerField(blank=True, null=True)
    ID_Role = models.ForeignKey(
        Roles,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    last_login = models.DateTimeField(blank=True, null=True)  # Add last_login field

    def __str__(self):
        return self.Username

    class Meta:
        db_table = 'Mod_Users'

    def save(self, *args, **kwargs):
        # Hash the password if it's not already hashed
        if not self.Password.startswith('pbkdf2_sha256$'):
            self.Password = make_password(self.Password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.Password)

    def set_password(self, raw_password):
        self.Password = make_password(raw_password)
        self.save()
               
class Predmet(models.Model):
    ID_Predmet = models.AutoField(primary_key=True)
    PredmetName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.PredmetName

class Courses(models.Model):
    ID_Course = models.AutoField(primary_key=True)
    Predmet = models.ForeignKey(Predmet, on_delete=models.SET_NULL, null=True, blank=True)
    Description = models.CharField(max_length=50000)
    CourseName = models.CharField(max_length=500)
    ID_User = models.ForeignKey(Mod_Users, on_delete=models.SET_NULL, null=True, blank=True)
    IsBlocked = models.BooleanField(default=False)
    IsSubscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.CourseName

class Topics(models.Model):
    ID_Topic = models.AutoField(primary_key=True)
    TopicName = models.CharField(max_length=100)
    ID_Course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.TopicName

from django.db import models
from django.core.exceptions import ValidationError

class Lectures(models.Model):
    ID_Lecture = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ID_Topic = models.ForeignKey(Topics, on_delete=models.CASCADE)

    def clean(self):
        if not self.Content.strip():
            raise ValidationError("Content cannot be empty.")

    def __str__(self):
        return self.Title
    
class Complexity(models.Model):
    ID_Complexity = models.AutoField(primary_key=True)
    ComplexityName = models.CharField(max_length=100)

    def __str__(self):
        return self.ComplexityName

class Levels(models.Model):
    ID_Level = models.AutoField(primary_key=True)
    LevelName = models.CharField(max_length=100)

    def __str__(self):
        return self.LevelName

class QuestionTypes(models.Model):
    ID_QuestionType = models.AutoField(primary_key=True)
    TypeName = models.CharField(max_length=50)

    def __str__(self):
        return self.TypeName

class Tests(models.Model):
    ID_Test = models.AutoField(primary_key=True)
    TestName = models.CharField(max_length=100)
    Description = models.TextField()
    ID_Complexity = models.ForeignKey(Complexity, on_delete=models.SET_NULL, null=True, blank=True)
    ID_Topic = models.ForeignKey(Topics, on_delete=models.CASCADE)

    def __str__(self):
        return self.TestName

class Questions(models.Model):
    ID_Question = models.AutoField(primary_key=True)
    QuestionText = models.TextField()
    correct_answer = models.TextField()
    wrong_answer = models.TextField()
    ID_Test = models.ForeignKey(Tests, on_delete=models.SET_NULL, null=True, blank=True)
    ID_QuestionType = models.ForeignKey(QuestionTypes, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.QuestionText

class UserCourses(models.Model):
    ID_User = models.ForeignKey(Mod_Users, on_delete=models.CASCADE)
    ID_Course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('ID_User', 'ID_Course'),)

    def __str__(self):
        return f"{self.ID_User} - {self.ID_Course}"

class TopicTests(models.Model):
    ID_Topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    ID_Test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('ID_Topic', 'ID_Test'),)

    def __str__(self):
        return f"{self.ID_Topic} - {self.ID_Test}"

class UserTests(models.Model):
    ID_UserTests = models.AutoField(primary_key=True)
    ID_User = models.ForeignKey(Mod_Users, on_delete=models.CASCADE)
    ID_Course = models.IntegerField()
    ID_Topic = models.IntegerField()
    ID_Test = models.IntegerField()
    TestName = models.CharField(max_length=100)
    Result = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    Grade = models.CharField(max_length=1, null=True, blank=True)
    DateTaken = models.DateTimeField()

    def __str__(self):
        return f"{self.ID_User} - {self.TestName}"