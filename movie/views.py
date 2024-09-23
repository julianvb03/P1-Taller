from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

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

def statistics_view(request):
    matplotlib.use('Agg')
    
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_count_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_count_by_year[year] = count

    plt.bar(range(len(movie_count_by_year)), movie_count_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(movie_count_by_year)), movie_count_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    movies = Movie.objects.all()
    movie_count_by_genre = {}

    for movie in movies:
        first_genre = movie.genre.split(',')[0].strip()
        if first_genre:
            if first_genre in movie_count_by_genre:
                movie_count_by_genre[first_genre] += 1
            else:
                movie_count_by_genre[first_genre] = 1
        else:
            if "None" in movie_count_by_genre:
                movie_count_by_genre["None"] += 1
            else:
                movie_count_by_genre["None"] = 1

    plt.bar(range(len(movie_count_by_genre)), movie_count_by_genre.values(), width=0.5, align='center')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(range(len(movie_count_by_genre)), movie_count_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic2 = base64.b64encode(image_png2).decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic, 'graphic2': graphic2})


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})