from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="first_name", required=True)
    last_name = forms.CharField(label="last_name", required=True)
    email = forms.EmailField(label="email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email') + tuple(UserCreationForm.Meta.fields)
        
        # 🎨 تعريب كاااامل لجميع الحقول بلا استثناء
        labels = {
            'username': 'username',
            'email':'email',
            'password1': 'password1',
            'password2': 'password2',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            # 🧹 تنظيف وحذف نصوص المساعدة الإنجليزية الطويلة والمشوهة في الصورة
            field.help_text = "" 
            
            # حقن التنسيقات الفخمة المنسقة
            field.widget.attrs.update({
                'class': 'form-control shadow-sm text-right px-3 py-2',
                'style': (
                    'direction: rtl; '
                    'text-align: right; '
                    'border: 1px solid #cbd5e1; '
                    'border-right: 4px solid #1e293b; ' # الخط الجانبي الكحلي الفخم
                    'border-radius: 8px; '
                    'border-top-right-radius: 0px; ' # حواف متناسقة تماماً مع الخط الجانبي
                    'border-bottom-right-radius: 0px; '
                    'font-size: 0.95rem; '
                    'color: #1e293b;'
                ),
                'placeholder': f'أدخل {field.label}...'
            })
class profileform(UserChangeForm):
    from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm # 👈 استدعاء فورم التعديل الجاهز

class ProfileForm(UserChangeForm):
    # 📦 1. كلاس الميتا لحاله للتحكم بحقول البروفايل المسموحة
    class Meta:
        model = User
        # تحديد الحقول الآمنة فقط والمسموح للمستخدم العادي أن يراها ويعدلها
        fields = ('first_name', 'last_name', 'username', 'email')
        
        # تعريب مسميات الحقول لتظهر بأناقة في الـ HTML
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الثاني (العائلة)',
            'username': 'اسم الحساب (المستخدم)',
            'email': 'البريد الإلكتروني المعتمد',
        }

    # 🛠️ 2. دالة البناء وتطهير الحقول وحقن التنسيق الفخم الخاص بكِ
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'password' in self.fields:
            del self.fields['password']
        # حلقة التكرار لحقن تنسيقات البوتستراب والهيكل العربي
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control shadow-sm mb-3 text-right px-3 py-2',
                'style': (
                    'direction: rtl; '
                    'text-align: right; '
                    'border: 1px solid #cbd5e1; '
                    'border-right: 4px solid #1e293b; ' # الخط الجانبي الكحلي الفخم الخاص بكِ
                    'border-radius: 8px; '
                    'border-top-right-radius: 0px; ' # حواف حادة متناغمة مع الخط
                    'border-bottom-right-radius: 0px; '
                    'font-size: 0.95rem; '
                    'color: #1e293b;'
                ),
                'placeholder': f'تحديث {field.label}...'
            })
