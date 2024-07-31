from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    searchTerm = request.GET.get('searchMovie')
    if searchTerm == None:
        movies = Movie.objects.all()
    else:
        movies = Movie.objects.filter(title__contains=searchTerm)
    context = {'searchTerm': searchTerm, 'movies': movies}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')