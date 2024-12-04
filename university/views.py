from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from .repositories import Repository
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
import pandas as pd
from django.views.decorators.clickjacking import xframe_options_exempt

@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
@csrf_exempt
def register_view(request):
    if request.method == 'GET':
        return render(request, 'auth/register.html')
    elif request.method == 'POST':
        data = request.POST
        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        password = data.get('password')
        age = data.get('age')

        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {'error': 'Email вже існує'})

        user = User.objects.create_user(
            email=email,
            name=name,
            surname=surname,
            age=age,
            password=password
        )

        return redirect('login')

@require_http_methods(["GET", "POST"])
@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        next_url = request.GET.get('next', '')
        return render(request, 'auth/login.html', {'next': next_url})
    elif request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        next_url = data.get('next')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            return render(request, 'auth/login.html', {'error': 'Невірний email або пароль', 'next': next_url})

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправлення на головну сторінку

# 1. Average Mark per Student per Subject
@api_view(['GET'])
def average_mark_per_student_per_subject(request):
    data = Repository.Marks.average_mark_per_student_per_subject()
    df = pd.DataFrame(list(data))
    # Rename columns for clarity
    df.rename(columns={
        'student__user_id': 'student_id',
        'student__user__name': 'student_name',
        'student__user__surname': 'student_surname',
        'subject__id': 'subject_id',
        'subject__name': 'subject_name'
    }, inplace=True)
    stats = df['average_mark'].describe().to_dict()
    return Response({'data': df.to_dict(orient='records'), 'stats': stats}, status=status.HTTP_200_OK)


# 2. Average Mark per Teacher
@api_view(['GET'])
def average_mark_per_teacher(request):
    data = Repository.Marks.average_mark_per_teacher()
    df = pd.DataFrame(list(data))
    # Rename columns for clarity
    df.rename(columns={
        'teacher__user_id': 'teacher_id',
        'teacher__user__name': 'name',
        'teacher__user__surname': 'surname'
    }, inplace=True)
    stats = df['average_mark'].describe().to_dict()
    return Response({'data': df.to_dict(orient='records'), 'stats': stats}, status=status.HTTP_200_OK)


# 3. Student Count per Group
@api_view(['GET'])
def student_count_per_group(request):
    data = Repository.StudentGroups.student_count_per_group()
    df = pd.DataFrame(list(data))
    stats = df['student_count'].describe().to_dict()
    return Response({'data': df.to_dict(orient='records'), 'stats': stats}, status=status.HTTP_200_OK)

# 4. Student Count per Subject
@api_view(['GET'])
def student_count_per_subject(request):
    data = Repository.Subjects.student_count_per_subject()
    df = pd.DataFrame(list(data))
    stats = df['student_count'].describe().to_dict()
    return Response({'data': df.to_dict(orient='records'), 'stats': stats}, status=status.HTTP_200_OK)

# 5. Students Count per Teacher
@api_view(['GET'])
def student_count_per_teacher(request):
    data = Repository.Teachers.student_count_per_teacher()
    df = pd.DataFrame(list(data))
    df.rename(columns={
        'user_id': 'teacher_id',
        'user__name': 'teacher_name',
        'user__surname': 'teacher_surname',
    }, inplace=True)
    stats = df['student_count'].describe().to_dict()
    return Response({
        'data': df.to_dict(orient='records'),
        'stats': stats
    }, status=status.HTTP_200_OK)

# 6. Average Mark per Exam
@api_view(['GET'])
def average_mark_per_exam(request):
    data = Repository.Exams.average_mark_per_exam()
    df = pd.DataFrame(list(data))
    stats = df['average_mark'].describe().to_dict()
    return Response({'data': df.to_dict(orient='records'), 'stats': stats}, status=status.HTTP_200_OK)

# Exam views
@api_view(["GET"])
def get_all_exams(request):
    exams = Repository.Exams.get_all()
    exams_data = [{"id": exam.id, "lesson": exam.lesson.id if exam.lesson else None, "max_value": exam.max_value} for exam in exams]
    return Response(exams_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_exam(request):
    data = request.data
    exam = Repository.Exams.create(lesson_id=data.get("lesson_id"), max_value=data.get("max_value"))
    return Response({"id": exam.id, "lesson": exam.lesson.id if exam.lesson else None, "max_value": exam.max_value}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_exam_by_id(request, exam_id):
    exam = Repository.Exams.get_by_id(exam_id)
    if exam:
        exam_data = {"id": exam.id, "lesson": exam.lesson.id if exam.lesson else None, "max_value": exam.max_value}
        return Response(exam_data, status=status.HTTP_200_OK)
    return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)


# Lesson views
@api_view(["GET"])
def get_all_lessons(request):
    lessons = Repository.Lessons.get_all()
    lessons_data = [{"id": lesson.id, "teacher": lesson.teacher.id if lesson.teacher else None, "subject": lesson.subject.id if lesson.subject else None} for lesson in lessons]
    return Response(lessons_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_lesson(request):
    data = request.data
    lesson = Repository.Lessons.create(
        teacher_id=data.get("teacher_id"),
        subject_id=data.get("subject_id"),
        time_schedule_lesson_number=data.get("time_schedule_lesson_number"),
        day=data.get("day"),
        group_id=data.get("group_id"),
        room_number=data.get("room_number")
    )
    return Response({"id": lesson.id, "teacher": lesson.teacher.id if lesson.teacher else None}, status=status.HTTP_201_CREATED)

@api_view(["GET"])

def get_lesson_by_id(request, lesson_id):
    lesson = Repository.Lessons.get_by_id(lesson_id)
    if lesson:
        lesson_data = {"id": lesson.id, "teacher": lesson.teacher.id if lesson.teacher else None}
        return Response(lesson_data, status=status.HTTP_200_OK)
    return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)


# Mark views
@api_view(["GET"])
def get_all_marks(request):
    marks = Repository.Marks.get_all()
    marks_data = [{"id": mark.id, "student": mark.student.id if mark.student else None, "value": mark.value} for mark in marks]
    return Response(marks_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_mark(request):
    data = request.data
    mark = Repository.Marks.create(
        student_id=data.get("student_id"),
        subject_id=data.get("subject_id"),
        value=data.get("value"),
        teacher_id=data.get("teacher_id"),
        mark_type=data.get("mark_type"),
        exam_id=data.get("exam_id"),
        lesson_id=data.get("lesson_id")
    )
    return Response({"id": mark.id, "value": mark.value}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_mark_by_id(request, mark_id):
    mark = Repository.Marks.get_by_id(mark_id)
    if mark:
        mark_data = {"id": mark.id, "value": mark.value}
        return Response(mark_data, status=status.HTTP_200_OK)
    return Response({"error": "Mark not found"}, status=status.HTTP_404_NOT_FOUND)


# Student views
@login_required(login_url='login')
@require_http_methods(["GET"])
def get_all_students(request):
    students = Repository.Students.get_all()
    return render(request, 'students/students_list.html', {'students': students})


@api_view(["POST"])
def create_student(request):
    data = request.data
    student = Repository.Students.create(id=data.get("user_id"), group_id=data.get("group_id"))
    return Response({"id": student.id, "group": student.group.name if student.group else None}, status=status.HTTP_201_CREATED)

@require_http_methods(["GET"])
def get_student_by_id(request, student_id):
    student = Repository.Students.get_by_id(student_id)
    if student:
        return render(request, 'students/student_detail.html', {'student': student})
    return render(request, 'error.html', {'message': 'Студента не знайдено'})

# StudentGroup views
@api_view(["GET"])
def get_all_student_groups(request):
    groups = Repository.StudentGroups.get_all()
    groups_data = [{"id": group.id, "name": group.name} for group in groups]
    return Response(groups_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_student_group(request):
    data = request.data
    group = Repository.StudentGroups.create(name=data.get("name"))
    return Response({"id": group.id, "name": group.name}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_student_group_by_id(request, group_id):
    group = Repository.StudentGroups.get_by_id(group_id)
    if group:
        group_data = {"id": group.id, "name": group.name}
        return Response(group_data, status=status.HTTP_200_OK)
    return Response({"error": "Student group not found"}, status=status.HTTP_404_NOT_FOUND)


# Subject views
@api_view(["GET"])
def get_all_subjects(request):
    subjects = Repository.Subjects.get_all()
    subjects_data = [{"id": subject.id, "name": subject.name, "credits": subject.credits} for subject in subjects]
    return Response(subjects_data, status=status.HTTP_200_OK)

@api_view(["POST"])

def create_subject(request):
    data = request.data
    subject = Repository.Subjects.create(name=data.get("name"), description=data.get("description"), credits=data.get("credits"))
    return Response({"id": subject.id, "name": subject.name, "credits": subject.credits}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_subject_by_id(request, subject_id):
    subject = Repository.Subjects.get_by_id(subject_id)
    if subject:
        subject_data = {"id": subject.id, "name": subject.name, "credits": subject.credits}
        return Response(subject_data, status=status.HTTP_200_OK)
    return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)


# Teacher views
@require_http_methods(["GET"])
def get_all_teachers(request):
    teachers = Repository.Teachers.get_all()
    return render(request, 'teachers/teachers_list.html', {'teachers': teachers})


@api_view(["POST"])
def create_teacher(request):
    data = request.data
    teacher = Repository.Teachers.create(id=data.get("user_id"), salary=data.get("salary"))
    return Response({"id": teacher.id, "salary": teacher.salary}, status=status.HTTP_201_CREATED)

@require_http_methods(["GET"])
def get_teacher_by_id(request, teacher_id):
    teacher = Repository.Teachers.get_by_id(teacher_id)
    if teacher:
        subjects = Repository.TeacherHasSubjects.get_subjects_by_teacher(teacher)
        return render(request, 'teachers/teacher_detail.html', {'teacher': teacher, 'subjects': subjects})
    return render(request, 'error.html', {'message': 'Вчителя не знайдено'})

# TimeSchedule views
@require_http_methods(["GET"])
def get_all_time_schedules(request):
    schedules = Repository.TimeSchedules.get_all()
    return render(request, 'time_schedules_list.html', {'schedules': schedules})

@api_view(["POST"])
def create_time_schedule(request):
    data = request.data
    schedule = Repository.TimeSchedules.create(lesson_number=data.get("lesson_number"), start_time=data.get("start_time"), end_time=data.get("end_time"))
    return Response({"lesson_number": schedule.lesson_number, "start_time": schedule.start_time, "end_time": schedule.end_time}, status=status.HTTP_201_CREATED)

@api_view(["GET"])

def get_time_schedule_by_id(request, lesson_number):
    schedule = Repository.TimeSchedules.get_by_id(lesson_number)
    if schedule:
        schedule_data = {"lesson_number": schedule.lesson_number, "start_time": schedule.start_time, "end_time": schedule.end_time}
        return Response(schedule_data, status=status.HTTP_200_OK)
    return Response({"error": "Time schedule not found"}, status=status.HTTP_404_NOT_FOUND)


# User views
@api_view(["GET"])
def get_all_users(request):
    users = Repository.Users.get_all()
    users_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return Response(users_data, status=status.HTTP_200_OK)

@api_view(["POST"])

def create_user(request):
    data = request.data
    user = Repository.Users.create(name=data.get("name"), middle_name=data.get("middle_name"), surname=data.get("surname"), email=data.get("email"), password_hash=data.get("password_hash"), age=data.get("age"))
    return Response({"id": user.id, "name": user.name, "email": user.email}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_user_by_id(request, user_id):
    user = Repository.Users.get_by_id(user_id)
    if user:
        user_data = {"id": user.id, "name": user.name, "email": user.email}
        return Response(user_data, status=status.HTTP_200_OK)
    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
