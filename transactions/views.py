from django.shortcuts import render, HttpResponse

# Create your views here.
def indexPage(request):
    return render(request, 'index.html'),