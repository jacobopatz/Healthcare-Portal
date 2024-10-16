# Django Info
This file is meant to share some of the information i've learned about django and how to utilize it's features.

## Project File Structure
You'll notice that there are multiple folders in the project folder. Each of these is considered a Django "app". Youll Recognize most of these are the different modules from our project. The other apps are described below:
1. [DjangoProject] This app is the base app that runs our program. It hangles things like loading the default webpage, managing all the different apps urls, and essentially is the app that runs the other apps
2. [login] This is the app that runs our user authentication, and serves as our homepage. This is actually fully functional as of right now so go ahead and make a username if you want!
3. [staticfiles]This is the one folder that actually does not represent an app. Instead, holds all the "static" files from the apps and compiles them into one place once the command python manage.py collectstatic is ran on the terminal. These files include the CSS and javascript code for each app. You'll notice that each app had a folder labeled statics, and this is where the framework is pulling these files from.
4. [License](#license)

## App File Structure
Once you open an apps folder, you'll see a series of files that are meant to run the app. Here I'll explain each files role and how they will contribute to the functionality of our project

1. [urls.py]: This is the file that declares the sub url's for this app. Django uses these url's to perform different functions within the app. Take the urls.py for the login app for example. The first argument is the actual url that will be displayed in the browser. You'll see the second argument for path() is a view, this is essentially the actions we want the website to take once loaded, that will be discussed later. The final argument is a name, this is the name we will use in the html code for each site to call a specific url and perform an action. If you look at the html code, you'll see  action="{% url 'login' %}. This code tells django to redirect to the login url, therefore executing the login view, which contains details on how to log the user in.
2. [views.py]: This file is essentially the java script that runs our app. Each URL has its own view, which describes the dynamic actions we would like our page to be able to make. Take the login url for example. When this is called, the middle argument calls the customlogin view, which then executes the get() command within this view. In this case, it is just rendering our login page with the provided html path. The second function in this view is post(). These are the functions that run once a form is submitted. I'll discuss forms next, but know they are esentially formatted fields of information on the wensite that the user can interact with, like the username and passwords. Once the form is submitted  using 
```html <form method="POST" action="{% url 'login' %}"> ```. This calls the login url's method named post, which 
3. [forms.py] This file describes forms for handeling user input, like defining a contact sheet or fields describing a search for available appointments. You can declare these here, and easily have them become available in on your website using something like this: 
```html
 {% csrf_token %}
 {{ form.as_p }} 
 ```
This is how we will get information from the user and search our models
4. [models.py] This is where we will define our models (which make up our database). We will be able to use the forms to search this and return data to the user
5.[Templates] This is a folder that essentially just holds our html files. Django has special features for processing html files. For example, if you look at any of the functional apps described in our project, youll see that their templates are using a base html template, so we do not have to re-write code for every page that uses the menu, for example.

## Installation
Navigate to the outer DjangoProject folder containing all of our app directories. Ensure you have python installed and run the following.

```bash
python manage.py runserver
```
If you change a css or js file, you'll have to run collect statics so django can compile these files into the static files folder. Use this command:
```bash
python manage.py collectstatic
```
