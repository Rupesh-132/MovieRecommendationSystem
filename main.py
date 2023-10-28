import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open("movie_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

similarity = pickle.load(open("similarity.pkl","rb"))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=04c783413abbff99fc468806dbcd0405&language=en-US"

    headers = {"accept": "application/json"}

    response = requests.get(url.format(movie_id), headers=headers)

    if response.status_code == 200:  # Checking if the response is successful (status code 200)
        try:
            data = response.json()
            poster_path = data.get('poster_path')

            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                return "Poster not available"

        except Exception as e:
            print("An error occurred:", e)
            return "Error fetching poster data"

    else:
        print("Request failed with status code:", response.status_code)
        return "Failed to fetch data"




def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = i[0]

        # Fetching the recommended movies poster
        recommended_movie_posters.append(fetch_poster(movie_id))
        # fetch the movie poster from api
        recommended_movies.append((movies.iloc[i[0]].title))

    return recommended_movies,recommended_movie_posters


selected_movie_name = st.selectbox(
    "Enter your movie name",
movies["title"].values
)

if st.button("Recommend"):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    st.write(recommended_movie_names)
    st.write(recommended_movie_posters)
    with col1:
        st.text(recommended_movie_names[0])
        #st.write(type(recommended_movie_posters[0]))
        if(recommended_movie_posters[0][0] == "h"):
            st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])

        if (recommended_movie_posters[1][0] == "h"):
            st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        if (recommended_movie_posters[2][0] == "h"):
            st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        if (recommended_movie_posters[3][0] == "h"):
            st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        if (recommended_movie_posters[4][0] == "h"):
            st.image(recommended_movie_posters[4])


