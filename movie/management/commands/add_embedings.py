from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        # Construir la ruta correcta al archivo JSON en el mismo directorio
        json_file_path = os.path.join(os.path.dirname(__file__), 'movie_descriptions_embeddings.json')

        # Verificar si el archivo JSON existe antes de abrirlo
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {json_file_path}"))
            return
        
        # Cargar los datos desde el archivo JSON
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        for movie in movies:
            emb = movie['embedding']
            emb_binary = np.array(emb).tobytes()
            item = Movie.objects.filter(title=movie['title']).first()
            if item:
                item.emb = emb_binary
                item.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully updated item embeddings'))
