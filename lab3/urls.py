"""
URL configuration for lab3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from university import views
from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('django_plotly_dash/', include(('django_plotly_dash.urls', 'django_plotly_dash'), namespace='the_django_plotly_dash')),
    path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
    path('bokeh_dashboard/', dashboard_views.bokeh_dashboard_view, name='bokeh_dashboard'),
    path('api/stats/average_mark_per_student_per_subject/', views.average_mark_per_student_per_subject, name='average_mark_per_student_per_subject'),
    path('api/stats/average_mark_per_teacher/', views.average_mark_per_teacher, name='average_mark_per_teacher'),
    path('api/stats/student_count_per_group/', views.student_count_per_group, name='student_count_per_group'),
    path('api/stats/student_count_per_subject/', views.student_count_per_subject, name='student_count_per_subject'),
    path('api/stats/student_count_per_teacher/', views.student_count_per_teacher, name='student_count_per_teacher'),
    path('api/stats/average_mark_per_exam/', views.average_mark_per_exam, name='average_mark_per_exam'),

    path("exams/", views.get_all_exams, name="get_all_exams"),
    path("exams/create/", views.create_exam, name="create_exam"),
    path("exams/<int:exam_id>/", views.get_exam_by_id, name="get_exam_by_id"),

    path("lessons/", views.get_all_lessons, name="get_all_lessons"),
    path("lessons/create/", views.create_lesson, name="create_lesson"),
    path("lessons/<int:lesson_id>/", views.get_lesson_by_id, name="get_lesson_by_id"),

    path("marks/", views.get_all_marks, name="get_all_marks"),
    path("marks/create/", views.create_mark, name="create_mark"),
    path("marks/<int:mark_id>/", views.get_mark_by_id, name="get_mark_by_id"),

    path("students/", views.get_all_students, name="get_all_students"),
    path("students/create/", views.create_student, name="create_student"),
    path("students/<int:student_id>/", views.get_student_by_id, name="get_student_by_id"),

    path("student-groups/", views.get_all_student_groups, name="get_all_student_groups"),
    path("student-groups/create/", views.create_student_group, name="create_student_group"),
    path("student-groups/<int:group_id>/", views.get_student_group_by_id, name="get_student_group_by_id"),

    path("subjects/", views.get_all_subjects, name="get_all_subjects"),
    path("subjects/create/", views.create_subject, name="create_subject"),
    path("subjects/<int:subject_id>/", views.get_subject_by_id, name="get_subject_by_id"),

    path("teachers/", views.get_all_teachers, name="get_all_teachers"),
    path("teachers/create/", views.create_teacher, name="create_teacher"),
    path("teachers/<int:teacher_id>/", views.get_teacher_by_id, name="get_teacher_by_id"),

    path("time-schedules/", views.get_all_time_schedules, name="get_all_time_schedules"),
    path("time-schedules/create/", views.create_time_schedule, name="create_time_schedule"),
    path("time-schedules/<int:lesson_number>/", views.get_time_schedule_by_id, name="get_time_schedule_by_id"),

    path("users/", views.get_all_users, name="get_all_users"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/<int:user_id>/", views.get_user_by_id, name="get_user_by_id"),

]
