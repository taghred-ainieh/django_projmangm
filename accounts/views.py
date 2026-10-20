from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm,ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
class Registerview(CreateView):
    form_class=CustomUserCreationForm
    template_name='registration/register.html'
    def get_success_url(self) :
        login(self.request,self.object)
        return reverse_lazy('project_list')

@login_required
def edit_profile(request):
    # 🟢 التصحيح الحاسم: إضافة .method للتحقق من نوع الطلب بشكل صحيح
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=request.user)
        
    # 💡 خطوة تنظيمية: جعل الـ render في النهاية تماماً ليعرض الاستمارة والأخطاء دائماً
    return render(request, 'profile.html', {'form': form})
