from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView
from projects.models import Project
# Create your views here.
class projectlistview(ListView):
    model=Project
    template_name='project/list.html'



class create_project(CreateView):
    model = Project                     
    fields=['title','descerptions','category']         
    template_name = 'project/create.html'
    success_url= reverse_lazy('project_list')    

