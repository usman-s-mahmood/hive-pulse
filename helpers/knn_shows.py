from .TMDB_API import get_tv_show_details, get_popular_shows
from MoviesApp.models import LikedShows
from django.contrib.auth.models import User
import math

GENRE_SET = {
    10759: 'Action & Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime',
    99: 'Documentary', 18: 'Drama', 10751: 'Family', 10762: 'Kids', 9648: 'Mystery',
    10763: 'News', 10764: 'Reality', 10765: 'Sci-Fi & Fantasy', 10766: 'Soap',
    10767: 'Talk', 10768: 'War & Politics', 37: 'Western'
}

def get_genre_vector(genre_ids):
    return [1 if gid in genre_ids else 0 for gid in GENRE_SET]

def euclidean_distance(vec1, vec2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

def build_feature_vector(tv_data):
    rating = tv_data.get('vote_average', 0)
    genre_vector = get_genre_vector(tv_data.get('genre_ids', []))
    return [rating] + genre_vector

def recommend_shows_knn(user: User, k=3, max_pool_size=20):
    liked = LikedShows.objects.filter(liked_by=user).order_by('-pk')
    liked_show_ids = [s.show_id for s in liked]
    liked_titles = [s.title for s in liked]

    liked_vectors = []
    for show_id in liked_show_ids:
        data = get_tv_show_details(show_id)
        if data:
            liked_vectors.append({
                'id': show_id,
                'title': data.get('name'),
                'poster_path': data.get('poster_path'),
                'vote_average': data.get('vote_average', 0),
                'vector': build_feature_vector(data)
            })

    if not liked_vectors:
        print("No liked TV shows found.")
        return []

    pool = get_popular_shows(page=1).get("results", [])[:max_pool_size]
    candidates = [
        {
            'id': s['id'],
            'title': s['name'],
            'poster_path': s.get('poster_path'),
            'vote_average': s.get('vote_average', 0),
            'vector': build_feature_vector(s)
        }
        for s in pool if s['id'] not in liked_show_ids
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

    for sid in similarity_scores:
        dists = similarity_scores[sid]['distances']
        similarity_scores[sid]['score'] = sum(dists) / len(dists)

    recommended = sorted(similarity_scores.items(), key=lambda x: x[1]['score'])

    print(f"\nTop {k} TV show recommendations for {user.username} (based on: {liked_titles})")
    top_recs = []
    for i, (sid, data) in enumerate(recommended[:k]):
        print(f"{i+1}. {data['title']} (⭐ {data['vote_average']}) | Score: {data['score']:.2f}")
        top_recs.append({
            'id': sid,
            'title': data['title'],
            'poster_path': data['poster_path'],
            'vote_average': data['vote_average']
        })

    return top_recs
