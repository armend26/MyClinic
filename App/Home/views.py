from django.shortcuts import render

# Create your views here.
def homeView(request):
    return render(request, 'Home/home.html')