import streamlit as st
import pickle
import pandas as pd
import requests
import sklearn

st.set_page_config(page_title='Movie Recommender System')
title = pickle.load(open('pklfiles/title.pkl','rb'))
id = pickle.load(open('pklfiles/movie_id.pkl','rb'))
similarity_mat = pickle.load(open('similarity.pkl','rb'))
movies = pd.concat([title,id],axis=1)
# st.write(movies)


def fetch_data(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=285383b6eb0b56baf7815a21b4f85b0e&language=en-US'
    response = requests.get(url)
    data = response.json()
    img_path = data['poster_path']
    path = "https://image.tmdb.org/t/p/w500"+img_path
    return path

def recommend(movie):
    ind = movies[movies['title']==movie].index[0]
    distances = similarity_mat[ind]
    movies_list = sorted(list((enumerate(distances))),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommend_movies_images = []
    for i in movies_list:
        # st.text(i)
        # Movies_id is useful to extract movies poster from TMDB API
        movie_id = movies.iloc[i[0]].id
        # st.write(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movies_images.append((fetch_data(movie_id)))    
    return recommended_movies,recommend_movies_images

    

st.title('Movie Recommendation System')

option = st.sidebar.selectbox(
    'Select Movies You Want',
    (movies['title'])
)
st.write('You Selcted : ',option)

id = movies[movies['title'] == option].id.values
st.image(fetch_data(id[0]))

if st.button('Recommend'):
    st.text('Recommended Movies ....')
    names,posters = recommend(option)
    col1,col2,col3,col4,col5= st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

    