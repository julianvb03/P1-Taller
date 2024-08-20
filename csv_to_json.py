import pandas as pd
import json

df = pd.read_csv('movies_initial.csv')

df.to_json('movies.json', orient='records')

with open('movies.json') as f:
    movies = json.load(f)

for i in range(10):
    movie = movies[i]
    print(movie)
