from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models
# Register your models here.
admin.site.register(models.Category)

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title','status','category','task_count']
    list_per_page=1
    list_editable=['status']
    list_select_related=['category']
    def task_count(self,obj):
        # return obj.task_set.count()
        return obj.task_count
    def get_queryset(self, request):
        query=super().get_queryset(request)
        query=query.annotate(task_count=Count('task'))
        return query


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=['id','description','project','is_completed']
    list_per_page=1
    list_editable=['is_completed']
    