from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect,render
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView,DeleteView
from projects.models import Project,Task
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# 👇 أضيفي هذا السطر في أعلى ملف views.py ليتعرف المحرر على الأمر
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = 'project/list.html' # أو اسم صفحة القائمة لديك
    paginate_by=3
    # 📌 الدالة السحرية لالتقاط كلمة البحث وفلترة البيانات ديناميكياً
    def get_queryset(self):
        query_set=super(). get_queryset()
        where={'user_id':self.request.user}
        # جلب الكلمة المكتوبة في صندوق البحث (إن وُجدت)
        q = self.request.GET.get('q')
        
        if q:
            # فلترة المشاريع: جلب أي مشروع يحتوي عنوانه (title) على الكلمة المكتوبة
            # يمكنك إضافة البحث في الوصف أيضاً عبر كتابة: | Q(description__icontains=query)
            return Project.objects.filter(Q(title__icontains=q))
            
        # إذا لم يكتب المستخدم شيئاً، يتم جلب كل المشاريع بشكل طبيعي
        return query_set.filter(**where)



class create_project(LoginRequiredMixin,CreateView):
    model = Project                     
    fields=['title','descerptions','category']         
    template_name = 'project/create.html'
    success_url= reverse_lazy('project_list')  

    def form_valid(self, form):
         form.instance.user =self.request.user
         return super().form_valid(form)



class update_project(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Project                       # 1. تحديد جدول قاعدة البيانات المطلوب
    fields=['title','descerptions','status']           # 2. تحديد الاستمارة المراد عرضها
    template_name = 'project/update.html' # 3. تحديد صفحة الـ HTML [1.5, 1.8]
    def get_success_url(self):
        # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
        # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
        return reverse('update_project', kwargs={'pk': self.object.pk})  
    def test_func(self) :
         return self.get_object().user==self.request.user


class create_task(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Task                     
    fields=['project','description']         
    template_name = 'project/task.html'
    http_method_names=['post']
    def test_func(self) :
       project_id=self.request.POST.get('project','')
       return Project.objects.get(pk=project_id).user_id==self.request.user.id
    def get_success_url(self):
            # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
            # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
            return reverse('update_project', kwargs={'pk': self.object.project.pk})  



class update_task(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Task                     
    fields=['is_completed']         
    http_method_names=['post']
    def test_func(self) :
           return self.get_object().project.user_id==self.request.user.id
    def get_success_url(self):
            # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
            # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
            return reverse('update_project', kwargs={'pk': self.object.project.pk})



class delete_task(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
     model=Task  
     def test_func(self) :
                return self.get_object().project.user_id==self.request.user.id
     def get_success_url(self):
                 # self.object يمثل المشروع الحالي الذي قام المستخدم بتعديله للتو
                 # نقوم بسحب الـ id (أو pk) الخاص به وتمريره للرابط
                 return reverse('update_project', kwargs={'pk': self.object.project.pk})



@login_required

def delete_project(request, pk):
    # جلب المشروع أو إظهار 404 إذا لم يكن موجوداً
    project = get_object_or_404(Project, pk=pk)
    
    # 🔥 الشرط السحري: إذا لم يكن المستخدم الحالي هو صاحب المشروع
    if project.user != request.user:
        raise PermissionDenied  # يرمي خطأ حماية 403 ويوقف الحذف فوراً!
    
    # إذا تجاوز الشرط بنجاح (يعني أنه صاحب المشروع) نكمل الحذف طبيعي:
    if request.method == 'POST':
        project.delete()
        messages.success(request, "تم حذف المشروع بنجاح!")
        return redirect(reverse('project_list')) 
        
    return render(request, 'project_confirm_delete.html', {'project': project})