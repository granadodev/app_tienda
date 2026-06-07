from django.shortcuts import render

# Create your views here.
def view_home(request):
    if request.method == "GET":
        return render(request, 'home.html')