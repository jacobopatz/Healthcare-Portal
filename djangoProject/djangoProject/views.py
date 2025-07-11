from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect

def load(request):
    return redirect(reverse_lazy('landing'))