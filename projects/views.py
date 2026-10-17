from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView,DeleteView
from projects.models import Project,Task
# Create your views here.
class projectlistview(ListView):
    model=Project
    template_name='project/list.html'



class create_project(CreateView):
    model = Project                     
    fields=['title','descerptions','category']         
    template_name = 'project/create.html'
    success_url= reverse_lazy('project_list')    



class update_project(UpdateView):
    model = Project                       # 1. تحديد جدول قاعدة البيانات المطلوب
    fields=['title','descerptions','status']           # 2. تحديد الاستمارة المراد عرضها
    template_name = 'project/update.html' # 3. تحديد صفحة الـ HTML [1.5, 1.8]
    def get_success_url(self):
        # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
        # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
        return reverse('update_project', kwargs={'pk': self.object.pk})  



class create_task(CreateView):
    model = Task                     
    fields=['project','description']         
    template_name = 'task/create.html'
    http_method_names=['post']
    success_url= reverse_lazy('project_list')   
    def get_success_url(self):
            # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
            # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
            return reverse('update_project', kwargs={'pk': self.object.project.pk})  



class update_task(UpdateView):
    model = Task                     
    fields=['is_completed']         
    http_method_names=['post']
    success_url= reverse_lazy('project_list')   
    def get_success_url(self):
            # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
            # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
            return reverse('update_project', kwargs={'pk': self.object.project.pk})



class delete_task(DeleteView):
     model=Task  
     def get_success_url(self):
                 # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
                 # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
                 return reverse('update_project', kwargs={'pk': self.object.project.pk})




class delete_project(DeleteView):
      model=Project
      success_url= reverse_lazy('project_list')    

