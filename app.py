import streamlit as st
import pandas as pd
import numpy as np
import random

DATA_URL = "pure_ratings2.csv"
st.title("Movie Recommender")
st.markdown("Tell me what you like, then I will find something for you.")
st.markdown("The results are purely based on ratings after individual user bias are removed.")
st.markdown("This tool uses data derived over 10 million user ratings and includes 10,577 movies.")

## Function definitions
@st.cache(persist=True, allow_output_mutation=True)
def load_data():
    data = pd.read_csv(DATA_URL,
                    dtype={
                        "UserID":str,
                        "Title": str,
                        "Genres": str
                        })
    return data

def show_function(list_length):
    ## Chaotic search, will be improved
    if list_length == 0:
        st.write('Sorry buddy, no movies for you')
    elif list_length == 1:
        st.write('After crazy calculations, I found only', list_length, 'movie for you.')
        st.write('Still, you can enjoy it:')
        st.write(selected_df.sample(1).Title.item())
    else:
        if mode_dict[mode_select] == 'mode1':
            st.write('After crazy calculations, I found', list_length, 'movies for you.')
            st.write('Since you asked for only one, try this:')
            st.write(selected_df.sample(1).Title.item())

        elif mode_dict[mode_select] == 'mode2':
            st.write('After crazy calculations, I found', list_length, 'movies for you.')
            st.write('Based on your choices, I come up with these', min(max(10, list_length), 10),  'movies:')
            title_try = selected_df.sample(min(max(10, list_length), 10))['Title']
            for i in range(len(title_try)):
                st.write(title_try.iloc[i])

## Main program

ready_data = load_data()
movie_pure_std = ready_data.Pure_Rating_avg.std()
selection = st.selectbox('Start typing your favourite movie below:',
                            list(ready_data.Title), index=100)

mode_dict = {"Just show me something" : 'mode1',
             "I'd like to see my options" : 'mode2'}

mode_select = st.radio("Would you like to see a single recommendation or a list?",
                        ('Just show me something', "I'd like to see my options"))

search_dict = {'Wide as Ocean' : 2,
               'Fair enough'   : 5,
               'To the point'  : 10}

search_coef = st.radio("By the way, how wide should I search?",
                        ('Wide as Ocean', 'Fair enough', 'To the point'), index=1)

selection_vicinity = [ready_data[ready_data["Title"] == selection].Pure_Rating_avg.item() - movie_pure_std/search_dict[search_coef],
                  ready_data[ready_data["Title"] == selection].Pure_Rating_avg.item() + movie_pure_std/search_dict[search_coef]]
selected_df = ready_data[ready_data["Pure_Rating_avg"].between(selection_vicinity[0],
                    selection_vicinity[1])].drop(labels=ready_data[ready_data["Title"] == selection].index)

if st.button('Bring it on!'):
    show_function(selected_df.shape[0])
else:
    st.write('Waiting for take off..')
