import pickle
import streamlit as st


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []

        for i in distances[1:6]:  
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names
    except IndexError:
        return ["Movie not found in the dataset!"]



st.header('🎥 Movie Recommender System')


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)

    if recommended_movie_names:
        
        st.markdown("#### Recommended Movies:")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; gap: 70px;">
                <div style="text-align: center; font-size: 18px; font-weight: bold;">{recommended_movie_names[0]}</div>
                <div style="text-align: center; font-size: 18px; font-weight: bold;">{recommended_movie_names[1]}</div>
                <div style="text-align: center; font-size: 18px; font-weight: bold;">{recommended_movie_names[2]}</div>
                <div style="text-align: center; font-size: 18px; font-weight: bold;">{recommended_movie_names[3]}</div>
                <div style="text-align: center; font-size: 18px; font-weight: bold;">{recommended_movie_names[4]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("No recommendations found!")
