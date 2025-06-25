from .TMDB_API import get_movie_details, get_popular_movies
from MoviesApp.models import LikedMovies
from django.contrib.auth.models import User
import math

GENRE_SET = {
    28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime',
    99: 'Documentary', 18: 'Drama', 10751: 'Family', 14: 'Fantasy', 36: 'History',
    27: 'Horror', 10402: 'Music', 9648: 'Mystery', 10749: 'Romance', 878: 'Sci-Fi',
    10770: 'TV Movie', 53: 'Thriller', 10752: 'War', 37: 'Western'
}

def get_genre_vector(genre_ids):
    return [1 if gid in genre_ids else 0 for gid in GENRE_SET]

def euclidean_distance(vec1, vec2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

def build_feature_vector(movie_data):
    rating = movie_data.get('vote_average', 0)
    genre_vector = get_genre_vector(movie_data.get('genre_ids', []))
    return [rating] + genre_vector

def recommend_movies_knn(user: User, k=3, max_pool_size=20):
    liked = LikedMovies.objects.filter(liked_by=user).order_by('-pk')
    liked_movie_ids = [m.movie_id for m in liked]
    liked_titles = [m.title for m in liked]

    liked_vectors = []
    for movie_id in liked_movie_ids:
        data = get_movie_details(movie_id)
        if data:
            liked_vectors.append({
                'id': movie_id,
                'title': data.get('title'),
                'poster_path': data.get('poster_path'),
                'vote_average': data.get('vote_average', 0),
                'vector': build_feature_vector(data)
            })

    if not liked_vectors:
        print("No liked movies found.")
        return []

    pool = get_popular_movies(page=1).get("results", [])[:max_pool_size]
    candidates = [
        {
            'id': m['id'],
            'title': m['title'],
            'poster_path': m.get('poster_path'),
            'vote_average': m.get('vote_average', 0),
            'vector': build_feature_vector(m)
        }
        for m in pool if m['id'] not in liked_movie_ids
    ]

    similarity_scores = {}
    for liked in liked_vectors:
        for cand in candidates:
            dist = euclidean_distance(liked['vector'], cand['vector'])
            similarity_scores.setdefault(
                cand['id'],
                {
                    'title': cand['title'],
                    'poster_path': cand['poster_path'],
                    'vote_average': cand['vote_average'],
                    'distances': []
                }
            )
            similarity_scores[cand['id']]['distances'].append(dist)

    for mid in similarity_scores:
        dists = similarity_scores[mid]['distances']
        similarity_scores[mid]['score'] = sum(dists) / len(dists)

    recommended = sorted(similarity_scores.items(), key=lambda x: x[1]['score'])

    print(f"\nTop {k} movie recommendations for {user.username} (based on: {liked_titles})")
    top_recs = []
    for i, (mid, data) in enumerate(recommended[:k]):
        print(f"{i+1}. {data['title']} (⭐ {data['vote_average']}) | Score: {data['score']:.2f}")
        top_recs.append({
            'id': mid,
            'title': data['title'],
            'poster_path': data['poster_path'],
            'vote_average': data['vote_average']
        })

    return top_recs
