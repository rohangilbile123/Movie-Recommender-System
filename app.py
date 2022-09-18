#Import necessary packages
import streamlit as st
import pickle
import pandas as pd
import requests

#Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)

#function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4aa5af79aa4a76c50b3767341151f4b2'.format(movie_id))
    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']


#function to recommend movies based on selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    #Create two list to store movies list and posters list
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
         movie_id=movies.iloc[i[0]].movie_id
         recommended_movies.append(movies.iloc[i[0]].title)
         #fetch poster
         recommended_movies_posters.append(fetch_poster(movie_id))
    return  recommended_movies, recommended_movies_posters


#Get data from the dump file and store in variables
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

#Display screen Code
st.title("Movie Recommendation System by Rohan Gilbile")
selected_movie_name = st.selectbox(
    'Select your movie from the list',
   movies['title'].values
)

#Button Code
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    #Display cards of name and poster
    col1, col2, col3, col4, col5 = st.columns(5)
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



#Display setting for footer and menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

