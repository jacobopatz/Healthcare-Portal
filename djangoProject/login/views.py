from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.views import View


# Custom login view
class customLogin(View):
    def get(self, request):
        return render(request, 'registration/login.html', {})

    def post(self, request):

        username = request.POST.get('username')  # Accessing the username field
        password = request.POST.get('password')  # Accessing the password field
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('landing')  # Redirect to a success page
        else:
            # Invalid login: add an error message to the context
            error_message = "Invalid username or password."
            return render(request, 'registration/login.html', { 'error': error_message})


# Registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def load(request):
    return redirect('login')


# A function to process the input text
def process_input_text(input_text):
    # Example: Reverse the input text as part of processing
    return input_text[::-1]


def index(request):
    return render(request, 'index.html')


def process_text(request):
    if request.method == 'POST':
        # Get the text input from the form
        input_text = request.POST.get('input_text')
        
        # Process the input text using the Python function
        processed_text = process_input_text(input_text)
        
        # Return the processed text in a simple response

class sched(View):
    def get(self,request):
        return render(request,'SCHED.html')
     
