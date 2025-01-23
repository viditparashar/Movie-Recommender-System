import pickle
import numpy as np
import streamlit as st


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []

        for i in distances[1:6]:  # Skip the first one (self)
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names
    except IndexError:
        return ["Movie not found in the dataset!"]


# Header
st.header('🎥 Movie Recommender System')

# Load Data
movies = pickle.load(open('movies.pkl', 'rb'))

# Load the first half of the similarity data
similarity_half_1 = pickle.load(open('similarity_part100000.pkl', 'rb'))
# Load the second half of the similarity data
similarity_half_2 = pickle.load(open('similarity_part200000.pkl', 'rb'))



# Check if the two halves have the same number of columns
if similarity_half_1.shape[1] == similarity_half_2.shape[1]:
    similarity = np.concatenate((similarity_half_1, similarity_half_2), axis=0)

else:

    st.stop()  # Stop execution if the error is triggered

# Get list of movies
movie_list = movies['title'].values

# Select a movie from the dropdown
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when button is pressed
if st.button('Show Recommendation'):
    if selected_movie:
        recommended_movie_names = recommend(selected_movie)

        if recommended_movie_names and recommended_movie_names[0] != "Movie not found in the dataset!":
            st.markdown("#### Recommended Movies:")
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; gap: 70px;">
                    {''.join([f'<div style="text-align: center; font-size: 18px; font-weight: bold;">{name}</div>' for name in recommended_movie_names])}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Movie not found in the dataset!")
    else:
        st.warning("Please select a movie!")
