import streamlit as st
import pandas as pd
import os
import home, random_page, favorites, go_crazy, cuisines
import pymongo
# import time
# import logging

# logging.basicConfig(level=logging.INFO)

@st.cache_resource
def get_mongo_client():
        return pymongo.MongoClient("mongodb+srv://tjsdylan0:kzQPOHODZ95Z6fIh@cluster0.1kbkoif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


@st.cache_data
def load_food_data():
    # Load the food data only once per session
    current_dir = os.path.dirname(__file__)  # Get the directory of the current file
    file_path = os.path.join(current_dir, "input", "recipes.csv")
    food_data = pd.read_csv(file_path)
    food_data.dropna(inplace=True)
    return food_data


def main():
    # start_time = time.time()
    # Initialize MongoDB connection and load data
    client = get_mongo_client()
    # logging.info(f"MongoDB connection established in {time.time() - start_time:.2f} seconds")

    db = client["NyomNyom"]
    collection = db["User"]
    # logging.info(f"Database accessed in {time.time() - start_time:.2f} seconds")


    # Load the food and ratings data only once and store them in session state
    if 'food_data' not in st.session_state:
        st.session_state.food_data = load_food_data()
    # logging.info(f"Food data loaded in {time.time() - start_time:.2f} seconds")
    food = st.session_state.food_data

    # Directory where images are stored
    # Get the directory of the current script
    current_dir = os.path.dirname(__file__)

    # Construct the absolute path to the image directory
    image_directory = os.path.join(current_dir, 'input', 'Food Images')

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Random", "Favourites", "GO CRAY CRAY", "Cuisines"])
    # logging.info(f"Tab options loaded in {time.time() - start_time:.2f} seconds")


    with tab1:
        home.display_home_tab(collection, image_directory, food)
        # logging.info(f"home data loaded in {time.time() - start_time:.2f} seconds")


    with tab2:
        random_page.display_random_tab(food, image_directory)
        # logging.info(f"home data loaded in {time.time() - start_time:.2f} seconds")


    with tab3:
        favorites.display_favourites_tab(collection, image_directory, food)
        # logging.info(f"fav data loaded in {time.time() - start_time:.2f} seconds")


    with tab4:

        go_crazy.display_crazy_tab(food)
        # logging.info(f"crazy data loaded in {time.time() - start_time:.2f} seconds")
                                           
    with tab5:
        cuisines.display_cuisine_tab(collection, image_directory, food)
        # logging.info(f"cuisine data loaded in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
