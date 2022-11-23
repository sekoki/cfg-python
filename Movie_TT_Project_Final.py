import random
import requests

print(" ______________________________ ")
print("|         Welcome to...        |")
print("|      Movies Top Trumps!      |")
print("|______________________________|")
print("")


API_URL = 'https://api.themoviedb.org/3'
#That's the basic URL you get in TMDB
API_KEY = 'faf74a5e4c12ee3f6f01e02f44bb84ff'
#What you get after the basic URL is the movie genre, below you find the number referring to specific genres
GENRE_IDS = {
    'action': 28,
    'comedy': 35,
    'horror': 27,
    'romance': 10749
}
#This is the code that will define the final 'url' called by the API, according to specific parameters
def call_api(path, params):
    #API url + path + parameters that we choose
    url = f'{API_URL}{path}'
    payload = {
        "api_key": API_KEY

    }
    payload.update(params)

    response = requests.get(url, params=payload)

    return response.json()

#This is the function that extracts the movies according to a genre, going through 10 pages of results
def fetch_movies(genre):
    # maxpages refers to what we get when we do a request, we know that there is at least 10 pages so we set it to 11
    maxpages = 11
    movies = []
    page = 1
    totalpages = 2
    #start of while loop which says that as long as the number of pages returned is lower than totalpages and maxpages (which is True), then the results of the pages after page 1 will be returned.
    while page < totalpages and page < maxpages:
        # the parameters to filter out adult content, but to include the genre of movies specified as well as the specific page of results
        params = {
            "include_adult": False,
            "with_genres": GENRE_IDS[genre],
            "page": page
        }
        result = call_api('/discover/movie', params)
        movies += result['results']

        #
        totalpages = result['total_pages']
        #page is being incremented by '1' in the loop
        page += 1 

    return movies
#This is the function that fetches a movie according to an 'id' as per the path below
def fetch_movie_card(id):
    path = f'/movie/{id}'
    movie = call_api(path, {})
    return {
        #start of dictionary with relevant keys and values to be returned so they can be compared against
        'title': movie['title'],
        'runtime': movie['runtime'],
        'budget': movie['budget'],
        'revenue': movie['revenue'],
        'audience_score': movie['vote_average']
    }
#This is the function that randomises the choice of movie being returned
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


#Start of game with a loop counting to 4 from 1, to enable 3 rounds

game_round = 4
for i in range(1, game_round):

    print(" | -----------------------------|")
    print(f"             Round {i}          ")
    print(" | -----------------------------|")
    print("")
    genre = input('Which genre of movie to play? (action, comedy, horror, romance) ')

    movies = fetch_movies(genre)
    movie1 = get_random_movie(movies)
    movie2 = get_random_movie(movies)

    print(f"Player 1 movie - {movie1['title']}")
    print(f"Player 2 movie - {movie2['title']}")
    print()

    stat = input("Which stat do you want to compare? (runtime, budget, revenue, audience_score) ")
    movie1_stat = movie1[stat]
    movie2_stat = movie2[stat]
    print()

    print(f"Player 1 movie - {movie1['title']} - {movie1_stat}")
    print(f"Player 2 movie - {movie2['title']} - {movie2_stat}")
    print()

    result_text = ''
    #conditional statements to choose a winner according to who has the highest 'score' in their stats
    if movie1_stat > movie2_stat:
        result_text = f'Round {i} - Player 1 wins'
        print('Player 1 wins!')

    elif movie2_stat > movie1_stat:
        result_text = f'Round {i} - Player 2 wins'
        print('Player 2 wins!')

    else:
        result_text = f"Round {i} - It's a draw for Player 1 & 2"
        print('Draw!')

    #The part that enables the storage of the results for the 3 rounds
    game_result = 'GameResults.txt'
    with open(game_result, 'a') as note_file:
        note_file.write(f"{result_text}\n")