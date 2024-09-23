from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construir la ruta completa al archivo JSON
        json_file_path = os.path.join(os.path.dirname(__file__), 'movie_descriptions.json')
        
        # Verificar si el archivo JSON existe antes de intentar abrirlo
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {json_file_path}"))
            return
        
        # Cargar los datos desde el archivo JSON
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        # Actualizar la base de datos
        cont = 0
        for movie in movies:
            movie_to_update = Movie.objects.filter(title=movie['title']).first()  # Asegurarse de que la película no exista ya en la BD
            if not movie_to_update:
                print(f"{movie['title']} is not in the database")
            else:
                movie_to_update.description = movie["description"]
                movie_to_update.save()
                cont += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {cont} descriptions to the database'))
