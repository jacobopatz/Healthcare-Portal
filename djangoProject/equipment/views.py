from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect

# Create your views here.
class equipment(View):
    def get(self,request):
        return render(request,'equipment.html',{})
   
