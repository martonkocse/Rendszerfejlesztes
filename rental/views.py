from django.shortcuts import render

def home(request):
    return render(request, "rental/index.html")