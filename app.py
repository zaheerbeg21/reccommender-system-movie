import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict = pickle.load(open('pickel_files/movie_dict.pkl', 'rb'))
similarity = pickle.load(open('pickel_files/similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


def fetch_posters(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    movie_overview = data['overview']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path, movie_overview


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    overview = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_posters(movie_id)[0])
        overview.append(fetch_posters(movie_id)[1])
    return recommended_movies, recommended_movies_posters, overview


st.title('Recommender System(Movies)')


movie_list = movies['title'].values
selected_movie_name = st.selectbox(
    "Choose movie",
    movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, overview = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        with st.expander("Read"):
            st.write(overview[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        with st.expander("Read"):
            st.write(overview[0])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        with st.expander("Read"):
            st.write(overview[0])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        with st.expander("Read"):
            st.write(overview[0])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        with st.expander("Read"):
            st.write(overview[0])
