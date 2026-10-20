from django.shortcuts import get_object_or_404, redirect,render
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView,DeleteView
from projects.models import Project,Task
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
# 👇 أضيفي هذا السطر في أعلى ملف views.py ليتعرف المحرر على الأمر
from django.contrib.auth.decorators import login_required

# Create your views here.
class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = 'project/list.html' # أو اسم صفحة القائمة لديك
    paginate_by=3
    # 📌 الدالة السحرية لالتقاط كلمة البحث وفلترة البيانات ديناميكياً
    def get_queryset(self):
        # جلب الكلمة المكتوبة في صندوق البحث (إن وُجدت)
        query = self.request.GET.get('q')
        
        if query:
            # فلترة المشاريع: جلب أي مشروع يحتوي عنوانه (title) على الكلمة المكتوبة
            # يمكنك إضافة البحث في الوصف أيضاً عبر كتابة: | Q(description__icontains=query)
            return Project.objects.filter(Q(title__icontains=query))
            
        # إذا لم يكتب المستخدم شيئاً، يتم جلب كل المشاريع بشكل طبيعي
        return Project.objects.all()



class create_project(LoginRequiredMixin,CreateView):
    model = Project                     
    fields=['title','descerptions','category']         
    template_name = 'project/create.html'
    success_url= reverse_lazy('project_list')    



class update_project(LoginRequiredMixin,UpdateView):
    model = Project                       # 1. تحديد جدول قاعدة البيانات المطلوب
    fields=['title','descerptions','status']           # 2. تحديد الاستمارة المراد عرضها
    template_name = 'project/update.html' # 3. تحديد صفحة الـ HTML [1.5, 1.8]
    def get_success_url(self):
        # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
        # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
        return reverse('update_project', kwargs={'pk': self.object.pk})  



class create_task(LoginRequiredMixin,CreateView):
    model = Task                     
    fields=['project','description']         
    template_name = 'project/task.html'
    http_method_names=['post']
  
    def get_success_url(self):
            # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
            # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
            return reverse('update_project', kwargs={'pk': self.object.project.pk})  



class update_task(LoginRequiredMixin,UpdateView):
    model = Task                     
    fields=['is_completed']         
    http_method_names=['post']
      
    def get_success_url(self):
            # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
            # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
            return reverse('update_project', kwargs={'pk': self.object.project.pk})



class delete_task(LoginRequiredMixin,DeleteView):
     model=Task  
     def get_success_url(self):
                 # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
                 # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
                 return reverse('update_project', kwargs={'pk': self.object.project.pk})



@login_required

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "تم حذف المشروع بنجاح!")
        # استخدام reverse يضمن جلب الرابط بشكل صحيح ويمنع المتصفح من البقاء في صفحة 404
        return redirect(reverse('project_list')) 
        
    return render(request, 'project_confirm_delete.html', {'project': project})

