from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect

# Create your views here.
class landing(View):
    def get(self,request):
        return render(request,'landing.html',{})
    def post(self,request):
         site = request.POST.get('site')
         return redirect(site)
