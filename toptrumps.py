import random
import requests

API_URL = 'https://api.themoviedb.org/3'
API_KEY = 'faf74a5e4c12ee3f6f01e02f44bb84ff'
GENRE_IDS = {
    'action': 28,
    'comedy': 35,
    'horror': 27,
    'romance': 10749
}

def call_api(path, params):
    url = f'{API_URL}{path}'
    payload = {
        "api_key": API_KEY
    }
    payload.update(params)

    response = requests.get(url, params=payload)
    return response.json()

def fetch_movies(genre):
    movies = []
    params = {
        "include_adult": False,
        "with_genres": GENRE_IDS[genre]
    }
    result = call_api('/discover/movie', params)
    movies += result['results']

    return movies

def fetch_movie_card(id):
    path = f'/movie/{id}'
    movie = call_api(path, {})
    return {
        'title': movie['title'],
        'runtime': movie['runtime'],
        'budget': movie['budget'],
        'revenue': movie['revenue'],
        'audience_score': movie['vote_average']
    }

def get_random_movie(movies):
    found = False
    while not found:
        selected = random.choice(movies)
        card = fetch_movie_card(selected['id'])
        found = True
        for value in card.values():
            if value == 0:
                found = False
    return card

genre = input('Which genre of movie to play? (action, comedy, horror, romance) ')

movies = fetch_movies(genre)
movie1 = get_random_movie(movies)
movie2 = get_random_movie(movies)

print(f"Player 1 movie - {movie1['title']}")
print(f"Player 2 movie - {movie2['title']}")
print()

stat = input('Which stat do you want to compare? (runtime, budget, revenue, audience_score) ')
movie1_stat = movie1[stat]
movie2_stat = movie2[stat]
print()

print(f"{movie1['title']} - {movie1_stat}")
print(f"{movie2['title']} - {movie2_stat}")
print()

if movie1_stat > movie2_stat:
    print('Player 1 wins!')
elif movie2_stat > movie1_stat:
    print('Player 2 wins!')
else:
    print('Draw!')