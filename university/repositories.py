from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Exam,
    Lesson,
    Mark,
    Student,
    StudentGroup,
    Subject,
    Teacher,
    TeacherHasSubject,
    TimeSchedule,
    User,
)
from django.db.models import Avg, Count


class BaseRepository:
    """Базовий репозиторій для CRUD операцій."""

    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        try:
            return self.model.objects.get(pk=obj_id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, obj_id, **kwargs):
        instance = self.get_by_id(obj_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
        return instance

    def delete(self, obj_id):
        instance = self.get_by_id(obj_id)
        if instance:
            instance.delete()
        return instance

class UsersRepository(BaseRepository):
    def exists_by_email(self, email):
        return self.model.objects.filter(email=email).exists()

    def get_by_email(self, email):
        try:
            return self.model.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

class TeacherHasSubjectsRepository(BaseRepository):
    def get_subjects_by_teacher(self, teacher):
        return Subject.objects.filter(teacherhassubject__teacher=teacher)

class MarksRepository(BaseRepository):
    def average_mark_per_student_per_subject(self):
        return self.model.objects.values(
            'student__user__id',
            'student__user__name',
            'student__user__surname',
            'subject__id',
            'subject__name'
        ).annotate(
            average_mark=Avg('value')
        ).order_by('student__user__id', 'subject__id')

    def average_mark_per_teacher(self):
        return self.model.objects.values(
            'teacher__user_id',
            'teacher__user__name',
            'teacher__user__surname'
        ).annotate(
            average_mark=Avg('value')
        ).order_by('-average_mark')

class StudentGroupsRepository(BaseRepository):
    def student_count_per_group(self):
        return self.model.objects.annotate(
            student_count=Count('student')
        ).values('id', 'name', 'student_count').order_by('-student_count')

    def average_mark_per_group(self):
        return self.model.objects.annotate(
            average_mark=Avg('student__mark__value')
        ).values(
            'id',
            'name',
            'average_mark'
        ).order_by('-average_mark')

class SubjectsRepository(BaseRepository):
    def student_count_per_subject(self):
        return self.model.objects.annotate(
            student_count=Count('mark__student', distinct=True)
        ).values('id', 'name', 'student_count').order_by('-student_count')

# repositories.py

from django.db.models.functions import ExtractWeek


class ExamsRepository(BaseRepository):
    def average_mark_per_exam(self):
        return self.model.objects.annotate(
            average_mark=Avg('mark__value')
        ).values('id', 'lesson__id', 'average_mark').order_by('-average_mark')

class StudentsRepository(BaseRepository):
    def students_with_average_mark(self):
        return self.model.objects.annotate(
            average_mark=Avg('mark__value')
        ).values('id', 'user__name', 'user__surname', 'average_mark').order_by('-average_mark')


class TeachersRepository(BaseRepository):
    def student_count_per_teacher(self):
        return self.model.objects.annotate(
            student_count=Count('lesson__group__student', distinct=True)
        ).values(
            'user_id',
            'user__name',
            'user__surname',
            'student_count'
        ).order_by('-student_count')


# Основний клас репозиторіїв для всіх моделей
class Repository:
    Exams = ExamsRepository(Exam)
    Lessons = BaseRepository(Lesson)
    Marks = MarksRepository(Mark)
    Students = StudentsRepository(Student)
    StudentGroups = StudentGroupsRepository(StudentGroup)
    Subjects = SubjectsRepository(Subject)
    Teachers = TeachersRepository(Teacher)
    TimeSchedules = BaseRepository(TimeSchedule)
    TeacherHasSubjects = TeacherHasSubjectsRepository(TeacherHasSubject)
    Users = UsersRepository(User)
