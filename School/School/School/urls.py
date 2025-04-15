"""
URL configuration for School project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django_prometheus import exports
from school_web.views import *
from django.http import HttpResponse

from prometheus_client import generate_latest
from django.http import HttpResponse


from django.http import JsonResponse
from django.views import View
from django.urls import path
from prometheus_client import make_wsgi_app
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def metrics_view(request):
    metrics = generate_latest()
    return HttpResponse(metrics, content_type=CONTENT_TYPE_LATEST)
urlpatterns = [
    path('metrics/', metrics_view),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', main_page),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('student/', student_view, name='student'),
    path('teacher/', teacher_view, name='teacher'),
    path('ad/', admin_view, name='ad'),
    path('manager/', manager_view, name='manager'),
    path('courses/', courses_view, name='courses'),
    path('courses/create/', create_course_view, name='create_course'),
    path('courses/update/<int:course_id>/', update_course_view, name='update_course'),
    path('courses/delete/<int:course_id>/', delete_course_view, name='delete_course'),
    path('courses/<int:course_id>/topics/', course_topics_view, name='course_topics'),
    path('courses/<int:course_id>/topics/create/', create_topic_view, name='create_topic'),
    path('courses/<int:course_id>/topics/update/<int:topic_id>/', update_topic_view, name='update_topic'),
    path('courses/<int:course_id>/topics/delete/<int:topic_id>/', delete_topic_view, name='delete_topic'),

    path('courses/<int:course_id>/topics/<int:topic_id>/tests/', tests_for_topic_view, name='tests_for_topic'),
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/create/', create_test_view, name='create_test'),  
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/update/', update_test_view, name='update_test'),
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/delete/', delete_test_view, name='delete_test'),

    
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/questions/', questions_for_test_view, name='questions_for_test'),
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/questions/create/', create_question_view, name='create_question'),
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/questions/create_multiple/', create_question_multiple_view, name='create_question_multiple'),
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/questions/create_text/', create_question_text_view, name='create_question_text'),

    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/questions/<int:question_id>/update/', update_question_view, name='update_question'),
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/<int:test_id>/questions/<int:question_id>/delete/', delete_question_view, name='delete_question'),

    #Лекция
    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/', lecture_list, name='lectures_for_topic'),
    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/create/', create_lecture, name='create_lecture'),
    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/<int:pk>/edit/', edit_lecture, name='edit_lecture'),
    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/<int:pk>/',lecture_detail, name='lecture_detail'),

    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/', lecture_list, name='lecture_list'),
    #Админ
    path('backup_database/', backup_database, name='backup_database'),

    path('all_stats_view/', all_stats_view, name='all_stats_view'),
    path('import_database/', import_database, name='import_database'),

    #Студент
    path('student/courses/', courses_list_view, name='courses_list'),
    path('courses/<int:course_id>/subscribe/', subscribe_course_view, name='subscribe_course'),
    path('student/subscribed_courses/', subscribed_courses_view, name='subscribed_courses'),
    path('student/course/<int:course_id>/', course_details_view, name='course_details'), 

    path('topic/<int:topic_id>/', topic_tests_view, name='topic_tests'), 
    path('courses/<int:course_id>/topics/<int:topic_id>/tests/', topic_tests_view, name='topic_tests_by_course'),
    path('topics/<int:topic_id>/tests/<int:test_id>/', start_test_view, name='start_test'),
    path('topics/<int:topic_id>/tests/<int:test_id>/submit/', test_submit, name='test_submit'), 
    
    
     path('student/testresults/', user_test_results, name='user_test_results'),
   

]