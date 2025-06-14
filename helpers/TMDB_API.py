import requests
import json
import random
from decouple import config
from datetime import datetime, timedelta

def top_3_movies():
    url = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc'

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config('TMDB')}"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        results = data.get('results', [])
        
        if len(results) < 3:
            sample_movies = [
                {
                    'adult': False,
                    'backdrop_path': '/a3F9cXjRH488qcOqFmFZwqawBMU.jpg',
                    'genre_ids': [16, 28, 878],
                    'id': 1376434,
                    'original_language': 'en',
                    'original_title': 'Predator: Killer of Killers',
                    'overview': (
                        "This original animated anthology follows three of the fiercest warriors in human history: "
                        "a Viking raider guiding her young son on a bloody quest for revenge, a ninja in feudal Japan "
                        "who turns against his Samurai brother in a brutal battle for succession, and a WWII pilot "
                        "who takes to the sky to investigate an otherworldly threat to the Allied cause."
                    ),
                    'popularity': 837.6076,
                    'poster_path': '/lbimIPTVsSlnmqSW5ngEsUxtHLM.jpg',
                    'release_date': '2025-06-05',
                    'title': 'Predator: Killer of Killers',
                    'video': False,
                    'vote_average': 8.0,
                    'vote_count': 333
                },
                {
                    'adult': False,
                    'backdrop_path': '/yBDvgpyynDsbMyK21FoQu1c2wYR.jpg',
                    'genre_ids': [9648, 80, 53],
                    'id': 870028,
                    'original_language': 'en',
                    'original_title': 'The Accountant²',
                    'overview': (
                        "When an old acquaintance is murdered, Wolff is compelled to solve the case. Realizing more extreme "
                        "measures are necessary, Wolff recruits his estranged and highly lethal brother, Brax, to help. In partnership "
                        "with Marybeth Medina, they uncover a deadly conspiracy, becoming targets of a ruthless network of killers "
                        "who will stop at nothing to keep their secrets buried."
                    ),
                    'popularity': 694.8593,
                    'poster_path': '/kMDUS7VmFhb2coRfVBoGLR8ADBt.jpg',
                    'release_date': '2025-04-23',
                    'title': 'The Accountant²',
                    'video': False,
                    'vote_average': 7.25,
                    'vote_count': 600
                },
                {
                    'adult': False,
                    'backdrop_path': '/7Zx3wDG5bBtcfk8lcnCWDOLM4Y4.jpg',
                    'genre_ids': [10751, 35, 878, 12],
                    'id': 552524,
                    'original_language': 'en',
                    'original_title': 'Lilo & Stitch',
                    'overview': (
                        "The wildly funny and touching story of a lonely Hawaiian girl and the fugitive alien "
                        "who helps to mend her broken family."
                    ),
                    'popularity': 492.6436,
                    'poster_path': '/Y6pjszkKQUZ5uBbiGg7KWiCksJ.jpg',
                    'release_date': '2025-05-17',
                    'title': 'Lilo & Stitch',
                    'video': False,
                    'vote_average': 7.1,
                    'vote_count': 577
                }
            ]

            print("Not enough TV show results to select from.")
            return  sample_movies


        # Randomly pick 3 unique movies
        selected_movies = random.sample(results, 3)

        movie_list = []
        for i, movie in enumerate(selected_movies):
            print(f"Movie {i+1} Title: {movie['original_title']}")
            print(f"\tOverview: {movie['overview']}")
            print(f"\tRating: {movie['vote_average']} ⭐")
            print(f"\tRelease Date: {movie['release_date']}\n")
            movie_list.append(movie)

        return movie_list
    except Exception as error:
        sample_movies = [
                {
                    'adult': False,
                    'backdrop_path': '/a3F9cXjRH488qcOqFmFZwqawBMU.jpg',
                    'genre_ids': [16, 28, 878],
                    'id': 1376434,
                    'original_language': 'en',
                    'original_title': 'Predator: Killer of Killers',
                    'overview': (
                        "This original animated anthology follows three of the fiercest warriors in human history: "
                        "a Viking raider guiding her young son on a bloody quest for revenge, a ninja in feudal Japan "
                        "who turns against his Samurai brother in a brutal battle for succession, and a WWII pilot "
                        "who takes to the sky to investigate an otherworldly threat to the Allied cause."
                    ),
                    'popularity': 837.6076,
                    'poster_path': '/lbimIPTVsSlnmqSW5ngEsUxtHLM.jpg',
                    'release_date': '2025-06-05',
                    'title': 'Predator: Killer of Killers',
                    'video': False,
                    'vote_average': 8.0,
                    'vote_count': 333
                },
                {
                    'adult': False,
                    'backdrop_path': '/yBDvgpyynDsbMyK21FoQu1c2wYR.jpg',
                    'genre_ids': [9648, 80, 53],
                    'id': 870028,
                    'original_language': 'en',
                    'original_title': 'The Accountant²',
                    'overview': (
                        "When an old acquaintance is murdered, Wolff is compelled to solve the case. Realizing more extreme "
                        "measures are necessary, Wolff recruits his estranged and highly lethal brother, Brax, to help. In partnership "
                        "with Marybeth Medina, they uncover a deadly conspiracy, becoming targets of a ruthless network of killers "
                        "who will stop at nothing to keep their secrets buried."
                    ),
                    'popularity': 694.8593,
                    'poster_path': '/kMDUS7VmFhb2coRfVBoGLR8ADBt.jpg',
                    'release_date': '2025-04-23',
                    'title': 'The Accountant²',
                    'video': False,
                    'vote_average': 7.25,
                    'vote_count': 600
                },
                {
                    'adult': False,
                    'backdrop_path': '/7Zx3wDG5bBtcfk8lcnCWDOLM4Y4.jpg',
                    'genre_ids': [10751, 35, 878, 12],
                    'id': 552524,
                    'original_language': 'en',
                    'original_title': 'Lilo & Stitch',
                    'overview': (
                        "The wildly funny and touching story of a lonely Hawaiian girl and the fugitive alien "
                        "who helps to mend her broken family."
                    ),
                    'popularity': 492.6436,
                    'poster_path': '/Y6pjszkKQUZ5uBbiGg7KWiCksJ.jpg',
                    'release_date': '2025-05-17',
                    'title': 'Lilo & Stitch',
                    'video': False,
                    'vote_average': 7.1,
                    'vote_count': 577
                }
            ]

        print("WARNING! TMDB API NOT WORKING for Movies query.")
        return  sample_movies


def get_previous_year_date_range():
    today = datetime.today()
    previous_year = today.year - 1
    start_date = f"{previous_year}-01-01"
    end_date = f"{previous_year}-12-31"
    return start_date, end_date


def top_3_tv_shows():
    start_date, end_date = get_previous_year_date_range()

    url = (
        f'https://api.themoviedb.org/3/discover/tv'
        f'?include_adult=false'
        f'&language=en-US'
        f'&sort_by=vote_average.desc'
        f'&vote_count.gte=100'
        f'&first_air_date.gte={start_date}'
        f'&first_air_date.lte={end_date}'
        f'&with_original_language=en'
        f'&with_origin_country=US|GB|CA|AU|IE|DE|FR|IT|NL|SE'
        f'&page=1'
    )

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config('TMDB')}"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        results = data.get('results', [])
        if len(results) < 3:
            sample_shows = [
                {
                    'adult': False,
                    'backdrop_path': '/3nmDXGCDcHbtP3Rw4vi9RD3cmmX.jpg',
                    'genre_ids': [16, 10759],
                    'id': 202284,
                    'origin_country': ['US'],
                    'original_language': 'en',
                    'original_name': 'Ninja Kamui',
                    'overview': 'A team of assassins exacts a bloody retribution on Joe Logan – a former ninja who escaped his clan – and his family for betraying their ancient code. Rising from his seeming "death," Joe will re-emerge as his former self – Ninja Kamui – to avenge his family and friends and bring down the very clan that made him.',
                    'popularity': 26.7416,
                    'poster_path': '/A7mYSloFonDcQtHTqyLqEg9rIkh.jpg',
                    'first_air_date': '2024-02-11',
                    'name': 'Ninja Kamui',
                    'vote_average': 8.32,
                    'vote_count': 302
                },
                {
                    'adult': False,
                    'backdrop_path': '/tuCU2yVRM2iZxFkpqlPUyvd6tSu.jpg',
                    'genre_ids': [16, 10759, 35, 10765],
                    'id': 94954,
                    'origin_country': ['US'],
                    'original_language': 'en',
                    'original_name': 'Hazbin Hotel',
                    'overview': "In attempt to find a non-violent alternative for reducing Hell's overpopulation, the daughter of Lucifer opens a rehabilitation hotel that offers a group of misfit demons a chance at redemption.",
                    'popularity': 38.9058,
                    'poster_path': '/rXojaQcxVUubPLSrFV8PD4xdjrs.jpg',
                    'first_air_date': '2024-01-18',
                    'name': 'Hazbin Hotel',
                    'vote_average': 8.7,
                    'vote_count': 1286
                },
                {
                    'adult': False,
                    'backdrop_path': '/Av4ku3UIoWBbxNxKjXrFohMS6xi.jpg',
                    'genre_ids': [18],
                    'id': 94028,
                    'origin_country': ['US'],
                    'original_language': 'en',
                    'original_name': 'RIPLEY',
                    'overview': "A grifter in 1960s New York is hired to convince a wealthy man's son to return home from Italy and begins a life of deceit, fraud and murder.",
                    'popularity': 21.1666,
                    'poster_path': '/rpSo8z9alultGVTqQ3dkLEyU8xx.jpg',
                    'first_air_date': '2024-04-04',
                    'name': 'RIPLEY',
                    'vote_average': 8.0,
                    'vote_count': 302
                }
            ]

            print("Not enough TV show results to select from.")
            return  sample_shows

        # Randomly pick 3 unique TV shows
        selected_shows = random.sample(results, 3)
        # print(f'{results}')
        tv_show_list = []
        for i, show in enumerate(selected_shows):
            print(f"TV Show {i+1} Title: {show['original_name']}")
            print(f"\tOverview: {show['overview']}")
            print(f"\tRating: {show['vote_average']} ⭐")
            print(f"\tFirst Air Date: {show['first_air_date']}\n")
            tv_show_list.append(show)

        return tv_show_list
    except Exception as error:
        sample_shows = [
                {
                    'adult': False,
                    'backdrop_path': '/3nmDXGCDcHbtP3Rw4vi9RD3cmmX.jpg',
                    'genre_ids': [16, 10759],
                    'id': 202284,
                    'origin_country': ['US'],
                    'original_language': 'en',
                    'original_name': 'Ninja Kamui',
                    'overview': 'A team of assassins exacts a bloody retribution on Joe Logan – a former ninja who escaped his clan – and his family for betraying their ancient code. Rising from his seeming "death," Joe will re-emerge as his former self – Ninja Kamui – to avenge his family and friends and bring down the very clan that made him.',
                    'popularity': 26.7416,
                    'poster_path': '/A7mYSloFonDcQtHTqyLqEg9rIkh.jpg',
                    'first_air_date': '2024-02-11',
                    'name': 'Ninja Kamui',
                    'vote_average': 8.32,
                    'vote_count': 302
                },
                {
                    'adult': False,
                    'backdrop_path': '/tuCU2yVRM2iZxFkpqlPUyvd6tSu.jpg',
                    'genre_ids': [16, 10759, 35, 10765],
                    'id': 94954,
                    'origin_country': ['US'],
                    'original_language': 'en',
                    'original_name': 'Hazbin Hotel',
                    'overview': "In attempt to find a non-violent alternative for reducing Hell's overpopulation, the daughter of Lucifer opens a rehabilitation hotel that offers a group of misfit demons a chance at redemption.",
                    'popularity': 38.9058,
                    'poster_path': '/rXojaQcxVUubPLSrFV8PD4xdjrs.jpg',
                    'first_air_date': '2024-01-18',
                    'name': 'Hazbin Hotel',
                    'vote_average': 8.7,
                    'vote_count': 1286
                },
                {
                    'adult': False,
                    'backdrop_path': '/Av4ku3UIoWBbxNxKjXrFohMS6xi.jpg',
                    'genre_ids': [18],
                    'id': 94028,
                    'origin_country': ['US'],
                    'original_language': 'en',
                    'original_name': 'RIPLEY',
                    'overview': "A grifter in 1960s New York is hired to convince a wealthy man's son to return home from Italy and begins a life of deceit, fraud and murder.",
                    'popularity': 21.1666,
                    'poster_path': '/rpSo8z9alultGVTqQ3dkLEyU8xx.jpg',
                    'first_air_date': '2024-04-04',
                    'name': 'RIPLEY',
                    'vote_average': 8.0,
                    'vote_count': 302
                }
            ]

        print("WARNING! TMDB API NOT WORKING for TV shows query.")
        return  sample_shows


import requests
from decouple import config

def get_movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config('TMDB')}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        movie_data = response.json()
        return movie_data
    
    except Exception as e:
        print(f"WARNING! TMDB API NOT WORKING for movie ID {movie_id}. Error: {e}")        
        return None


if __name__ == '__main__':
    print("Random Top 3 Movies:\n")
    top_3_movies()

    print("\nRandom Top 3 TV Shows:\n")
    top_3_tv_shows()
    print(f'===========================================================================')
    print(f'Details for Movie ID: {870028}')
    print(f'===========================================================================')
    print(get_movie_details(870028))
