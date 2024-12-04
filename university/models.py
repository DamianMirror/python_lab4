from django.db import models

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, surname, age, password=None):
        if not email:
            raise ValueError('Email повинен бути встановлений')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, age=age)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, age, password):
        user = self.create_user(email, name, surname, age, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    email = models.EmailField(unique=True, max_length=250)
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'age']

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'
        managed = False



class Exam(models.Model):
    lesson = models.ForeignKey('Lesson', models.DO_NOTHING)
    max_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'exam'


class Lesson(models.Model):
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    subject = models.ForeignKey('Subject', models.DO_NOTHING)
    time_schedule_lesson_number = models.IntegerField()
    day = models.DateTimeField()
    group = models.ForeignKey('StudentGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lesson'


class Mark(models.Model):
    student = models.ForeignKey('Student', models.DO_NOTHING)
    subject = models.ForeignKey('Subject', models.DO_NOTHING)
    value = models.IntegerField()
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mark'


class Student(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, db_column='id', primary_key=True)
    group = models.ForeignKey('StudentGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student'


class StudentGroup(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'student_group'


class Subject(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'subject'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, db_column='id', primary_key=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'teacher'

    # Додайте наступне для зручного доступу до предметів
    @property
    def subjects(self):
        return Subject.objects.filter(teacherhassubject__teacher=self)


class TeacherHasSubject(models.Model):
    teacher = models.ForeignKey('university.Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('university.Subject', on_delete=models.CASCADE)

    class Meta:
        db_table = 'teacher_has_subject'
        managed = False  # Since you're manually managing the table


class TimeSchedule(models.Model):
    lesson_number = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'time_schedule'



