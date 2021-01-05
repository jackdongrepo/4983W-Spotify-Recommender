from lib import audio_methods
import pandas as pd
from sklearn.cluster import KMeans

normalized_feature_stats = pd.read_csv("./data_frames/normalized_feature_stats.csv",
                                       usecols = range(0,10), index_col = 0)
mean_stats = normalized_feature_stats.mean()
std_stats = normalized_feature_stats.std()

# KMeans of K=400
kmeans = KMeans(n_clusters=400,random_state=4983).fit(normalized_feature_stats)

# DF of each track's clusters based on kmeans model
all_cluster_family = pd.DataFrame({
    'track':normalized_feature_stats.index,
    'cluster_id':kmeans.labels_
})

"""
Usage:

from lib import recommender

recommender.recommend('Alvaro Soler Loca')
"""
def recommend(description,n=10):
    """
    Uses Spotify search function to find closest related track to user's input description,
    Returns n number of recommended samples
    
    Inputs:
    - Description, user input string describing song title, artist
    - n, number of recommended songs desired, defaults to 10
    
    Returns:
    - Print statement of n recommends based on what Spotify found with user input description
    """
    
    try:
        # Find audio features of user input track
        base_track = audio_methods.findTrack(description)
        base_track_features = audio_methods.getAudioFeatures(base_track)
    except:
        return print("Error: -1. Track not found, try another track.")

    # Format features into df to prep for model prediction
    base_track_features_df = pd.DataFrame({
        'danceability':base_track_features['danceability'],
        'energy':base_track_features['energy'],
        'loudness':base_track_features['loudness'],
        'speechiness':base_track_features['speechiness'],
        'acousticness':base_track_features['acousticness'],
        'instrumentalness':base_track_features['instrumentalness'],
        'liveness':base_track_features['liveness'],
        'valence':base_track_features['valence'],
        'tempo':base_track_features['tempo']
    },index=[0])

    # Normalize user input track and predict using model
    normalized_base_track = (base_track_features_df-mean_stats)/std_stats
    base_track_cluster = kmeans.predict(normalized_base_track)[0]

    # Return N tracks in recommended cluster
    recommends = all_cluster_family[all_cluster_family.cluster_id == base_track_cluster].sample(n).track

    # Return string of title, artists of recommends
    final_string = "\r\nYou listened to: " + audio_methods.getNameOfTrack(base_track) + " by "
    final_string += audio_methods.getArtistOfTrack(base_track) + "\r\n\r\n"
    final_string += "We recommend (not ordered):\r\n"
    for sng in recommends:
        track_name = audio_methods.getNameOfTrack(sng)
        artist_name = audio_methods.getArtistOfTrack(sng)
        final_string += "- " + track_name + " by " + artist_name + "\r\n"
    return print(final_string)