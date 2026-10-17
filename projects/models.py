from django.db import models


from django.contrib.auth.models import User

# 1. جدول المستخدم (User)
# نستخدم AbstractUser لأن الجدول يحتوي على الحقول الأساسية مع حقول مخصصة
from django.conf.global_settings import AUTH_USER_MODEL

# 2. جدول التصنيفات (Category)
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class ProjectStatus(models.IntegerChoices):
        PENDING = 1, 'PENDING'
        COMPLETED = 2, 'COMPLETED'
        POSTPONED = 3, 'POSTPONED'
        CANCELED = 4, 'CANCELED'

# 3. جدول المشاريع (Project)
class Project(models.Model):
    # تعريف الـ Enum لحالات المشروع كما هو موضح في المخطط
   

    title = models.CharField(max_length=255)
    descerptions=models.TextField()
    status=models.IntegerField(
        choices=ProjectStatus.choices,
        default=ProjectStatus.PENDING
    )
    status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # العلاقات (Foreign Keys)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 4. جدول المهام (Task)
class Task(models.Model):
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    
    # العلاقة مع المشروع (Foreign Key)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task {self.description} for Project {self.project.title}"
