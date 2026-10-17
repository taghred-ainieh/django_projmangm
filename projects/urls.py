from django.urls import path
from . import views # استيراد ملف الـ views الخاص بالتطبيق

# تأكدي من الاسم بالحرف الواحد كالتالي (كل الحروف صغيرة وفي نهايتها s):
urlpatterns = [
    # ضعي مسارات الروابط الخاصة بكِ هنا، على سبيل المثال:
    path('', views.projectlistview.as_view(), name='project_list'),
    path('project/create', views.create_project.as_view(), name='create_projecr'),
]
