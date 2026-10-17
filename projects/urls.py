from django.urls import path
from . import views # استيراد ملف الـ views الخاص بالتطبيق

# تأكدي من الاسم بالحرف الواحد كالتالي (كل الحروف صغيرة وفي نهايتها s):
urlpatterns = [
    # ضعي مسارات الروابط الخاصة بكِ هنا، على سبيل المثال:
    path('', views.projectlistview.as_view(), name='project_list'),
    path('project/create', views.create_project.as_view(), name='create_projecr'),
    path('project/update/<int:pk>', views.update_project.as_view(), name='update_project'),
    path('task/create', views.create_task.as_view(), name='create_task'),
    path('task/delete/<int:pk>', views.delete_task.as_view(), name='delete_task'),
    path('project/delete/<int:pk>', views.delete_project.as_view(), name='delete_project'),
    path('task/update/<int:pk>', views.update_task.as_view(), name='update_task'),
]
