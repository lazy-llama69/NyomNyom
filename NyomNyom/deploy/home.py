import streamlit as st
import os
import pandas as pd
import json


def display_home_tab(collection, image_directory, food):
    username = st.session_state.get('username', None)
    st.title("Welcome back " + username + " 👋🏻")

    # Initialize session state for selected food and view index
    if 'selected_food' not in st.session_state:
        st.session_state.selected_food = None

    def switch_to_details(food_title, food_index):
        st.session_state.selected_food = {'title': food_title, 'index': food_index}

    def switch_to_search():
        st.session_state.selected_food = None

    def display_search_results(filtered_food,image_directory):
        if not filtered_food.empty:
            N_cards_per_row = 3 
            for n_row, row in filtered_food.reset_index().iterrows():
                i = n_row % N_cards_per_row
                if i == 0:
                    st.write("---")
                    cols = st.columns(N_cards_per_row, gap="large")

                with cols[i]:
                    image_path = os.path.join(image_directory, row['Image_Name'] + '.jpg')

                    if os.path.exists(image_path):
                        st.image(image_path, use_column_width=True)
                    else:
                        st.error(f"Image not found: {row['Image_Name']}")

                    st.markdown(f"**{row['Title'].strip()}**")

                    if st.button(row['Title'], key=row['Index']):
                        switch_to_details(row['Title'], row['Index'])  # Pass title and index
                        st.session_state.selected_food = {'title': row['Title'], 'index': row['Index']}


    def display_recommendations(recommendations, food, image_directory):
        N_cards_per_row = 3# Number of cards per row
        for n_row, rec_item in enumerate(recommendations):
            # Filter by both title and index
            recommended_food_item = food[
                (food['Title'] == rec_item['title']) & (food['Index'] == rec_item['index'])]

            if recommended_food_item.empty:
                st.warning(f"No food item found with the title '{rec_item['title']}'")
                continue# Skip to the next recommendation if no match is foundelse:
            recommended_food_item = recommended_food_item.iloc[0]
            image_path = os.path.join(image_directory, recommended_food_item['Image_Name'] + '.jpg')

            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")

            with cols[i]:
                if os.path.exists(image_path):
                    st.image(image_path, use_column_width=True)
                else:
                    st.error(f"Image not found: {recommended_food_item['Image_Name']}")

                # Clickable food title with a unique key
                unique_key = f"{rec_item['title']}_{rec_item['index']}"
                if st.button(recommended_food_item['Title'], key=unique_key):
                    st.session_state.selected_food = {'title': recommended_food_item['Title'], 'index': recommended_food_item['Index']}
                    # Call a function to update the display instead of rerun
                    display_selected_food_details(recommended_food_item, image_directory)

    def display_selected_food_details(food_item, image_directory):
        image_path = os.path.join(image_directory, food_item['Image_Name'] + '.jpg')

        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.error(f"Image not found: {food_item['Image_Name']}")

        st.markdown(f"## {food_item['Title']}")
        st.markdown(f"**Ingredients:** {food_item['Ingredients']}")
        st.markdown(f"**Instructions:** {food_item['Instructions']}")

    # Display the current view
    if st.session_state.selected_food is None:
        # Search and recommendation view
        st.subheader("What do you feel like eating today? 🍴")
        st.subheader("🍔 🍜 🍱 🌮 🥟 🍣 🥞 🧋 🍰 🥐 🥗 🍲 🍛")

        # List of common allergens
        allergens = ["Gluten", "Peanuts", "Tree Nuts", "Dairy", "Soy", "Eggs", "Fish", "Shellfish"]

        # Multiselect for allergens
        selected_allergens = st.multiselect("Select Allergens to Avoid", allergens, key="selected_allergens")

        # Add a radio button group for choosing search criteria
        search_by = st.radio(
            "Search by:",
            ("Title", "Ingredients"),
            key="search_by"
        )

        search_term = st.text_input("Search for a food item or ingredient:", key="search_term")

        
        allergen_mapping = {
            "Gluten": ["bread", "pasta", "flour", "wheat", "barley", "rye", "bulgur", "farro", "graham", "kamut", "matzo",
                "semolina", "spelt", "triticale", "bran", "spaghetti", "macaroni", "fettuccine", "linguine", "penne", "psyllium husks"],
            "Peanuts": ["peanuts", "peanut butter", "peanut oil", "groundnut"],
            "Dairy": ["milk", "cheese", "butter", "cream", "yogurt", "buttermilk", "ghee", "whey", "casein", "custard",
                    "ice cream", "cotijia", "parmesan"],
            "Soy": ["soy", "soy sauce", "tofu", "tempeh", "edamame", "miso", "soy protein", "soy lecithin", "soya milk"],
            "Eggs": ["eggs", "egg whites", "mayonnaise", "albumin", "meringue", "ovalbumin"],
            "Fish": ["salmon", "tuna", "cod", "haddock", "tilapia", "mackerel", "sardines", "anchovies", "herring", "bass"],
            "Shellfish": ["shrimp", "crab", "lobster", "clams", "oysters", "mussels", "scallops", "prawns", "crawfish",
                        "abalone"],
            "Tree Nuts": ["almonds", "walnuts", "pecans", "cashews", "hazelnuts", "macadamia nuts", "pistachios", "brazil nuts",
                        "pine nuts", "chestnuts"]
        }

        # Display results only if a search term is entered
        if search_term:
            if search_by == "Title":
                # Search by Title
                filtered_food = food[food['Title'].str.contains(search_term, case=False, na=False)].head(18)
            elif search_by == "Ingredients":
                # Search by Ingredients
                filtered_food = food[food['Ingredients'].str.contains(search_term, case=False, na=False)].head(18)

            # Filter by allergens
            if selected_allergens:
                allergen_filtered_food = []

                def contains_allergen_ingredients(ingredients, allergens, allergen_mapping):
                    ingredients_lower = [ingredient.lower() for ingredient in ingredients]
                    
                    for allergen in allergens:
                        related_ingredients = allergen_mapping.get(allergen, [])
                        related_ingredients_lower = [ri.lower() for ri in related_ingredients]

                        for ingredient in ingredients_lower:
                            for related in related_ingredients_lower:
                                if related in ingredient:
                                    return True
                    return False

                for idx, row in filtered_food.iterrows():
                    ingredients = row['Ingredients']
                    # Ensure ingredients are a list
                    if isinstance(ingredients, str):
                        try:
                            ingredients = eval(ingredients)  # Safely evaluate string to list
                        except:
                            continue  # Skip this item if ingredients are not correctly formatted
                    
                    # Check if the food item contains any of the selected allergens
                    if not contains_allergen_ingredients(ingredients, selected_allergens, allergen_mapping):
                        allergen_filtered_food.append(row)

                filtered_food = pd.DataFrame(allergen_filtered_food)


            display_search_results(filtered_food,image_directory)
            

        # Display recommendations below the search bar
        st.subheader("Recommended Meals Based on Your Favorites")

        if username:
            user = collection.find_one({"username": username})
            favorite_titles = user.get("favorites", [])

            # print(f"selected_allergens before recommending: {selected_allergens}")
            recommendations = food_recommendation_from_precomputed(food, favorite_titles, 9, selected_allergens)
            # print(recommendations)
            if recommendations:
                display_recommendations(recommendations,food, image_directory)
    else:
        # Unified Details view
        selected_food_item = food[(food['Index'] == st.session_state.selected_food['index']) &
                                  (food['Title'] == st.session_state.selected_food['title'])]
        if not selected_food_item.empty:
            food_item = selected_food_item.iloc[0]

            image_path = os.path.join(image_directory, food_item['Image_Name'] + '.jpg')

            if os.path.exists(image_path):
                st.image(image_path, use_column_width=True)
            else:
                st.error(f"Image not found: {image_path}")

            st.markdown(f"## {food_item['Title']}")
            st.markdown(f"**Ingredients:** {food_item['Ingredients']}")
            st.markdown(f"**Instructions:** {food_item['Instructions']}")

            # Add to Favorites Button
            if st.button("Add to Favorites 🩷"):
                if st.session_state['logged_in_user']:
                    username = st.session_state['logged_in_user']
                    add_to_favorites(collection, username, food_item['Title'], food_item["Index"])
                    st.success(f"{food_item['Title']} has been added to your favorites! 😉")

            if st.button("Go back"):
                switch_to_search()  # Switch back to the Search view
                st.session_state['selected_food'] = None# Clear the selected food to return to the search viewelse:
        else:
            st.error("The selected food item could not be found.")
            if st.button("Go back"):
                switch_to_search()
                st.session_state['selected_food'] = None# Clear the selected food to return to the search view





def load_precomputed_recommendations():
    with open("precomputed_recommendations.json", "r") as f:
        return json.load(f)


precomputed_recommendations = load_precomputed_recommendations()

def food_recommendation_from_precomputed(food, favorite_items=None, top_n=9, selected_allergens=None, allergen_mapping=None):
    if favorite_items is None:
        favorite_items = []

    if selected_allergens is None:
        selected_allergens = []

    if allergen_mapping is None:
        allergen_mapping = {
            "Gluten": ["bread", "pasta", "flour", "wheat", "barley", "rye", "bulgur", "farro", "graham", "kamut", "matzo",
                "semolina", "spelt", "triticale", "bran", "spaghetti", "macaroni", "fettuccine", "linguine", "penne"],
            "Peanuts": ["peanuts", "peanut butter", "peanut oil", "groundnut"],
            "Dairy": ["milk", "cheese", "butter", "cream", "yogurt", "buttermilk", "ghee", "whey", "casein", "custard",
                    "ice cream"],
            "Soy": ["soy", "soy sauce", "tofu", "tempeh", "edamame", "miso", "soy protein", "soy lecithin", "soya milk"],
            "Eggs": ["eggs", "egg whites", "mayonnaise", "albumin", "meringue", "ovalbumin"],
            "Fish": ["salmon", "tuna", "cod", "haddock", "tilapia", "mackerel", "sardines", "anchovies", "herring", "bass"],
            "Shellfish": ["shrimp", "crab", "lobster", "clams", "oysters", "mussels", "scallops", "prawns", "crawfish",
                        "abalone"],
            "Tree Nuts": ["almonds", "walnuts", "pecans", "cashews", "hazelnuts", "macadamia nuts", "pistachios", "brazil nuts",
                        "pine nuts", "chestnuts"]
        }


    all_recommendations = []

    for favorite in favorite_items:
        food_index = favorite['index']
        if str(food_index) in precomputed_recommendations:
            all_recommendations.extend(precomputed_recommendations[str(food_index)])
        else:
            st.write(f"Warning: No precomputed recommendations found for index {food_index}")

    favorite_set = set((fav['title'], fav['index']) for fav in favorite_items)

    filtered_recommendations = [
        rec for rec in all_recommendations
        if (rec['title'], rec['index']) not in favorite_set
    ]

    def contains_allergen_ingredients(ingredients, allergens, allergen_mapping):
        ingredients_lower = [ingredient.lower() for ingredient in ingredients]
        
        for allergen in allergens:
            related_ingredients = allergen_mapping.get(allergen, [])
            related_ingredients_lower = [ri.lower() for ri in related_ingredients]

            for ingredient in ingredients_lower:
                for related in related_ingredients_lower:
                    if related in ingredient:  # Check if any related ingredient is a substring of the ingredient
                        # print(f"Matching ingredient: {ingredient}")
                        # print(f"Found allergen '{related}' in ingredient '{ingredient}'")
                        return True
        return False

    allergen_free_recommendations = []

    for rec in filtered_recommendations:
        food_index = rec['index']
        if not food.loc[food['Index'] == food_index, 'Ingredients'].empty:
            ingredients = food.loc[food['Index'] == food_index, 'Ingredients'].values[0]
            
            # Ensure ingredients are a list
            if isinstance(ingredients, str):
                # print(f"Converting ingredients from string to list for {rec['title']}")
                try:
                    ingredients = eval(ingredients)  # Safely evaluate string to list
                    # print("it does go here")
                except:
                    print(f"Failed to parse ingredients: {ingredients}")
                    continue  # Skip this item if ingredients are not correctly formatted
            
            # print(f"Checking food item: {rec['title']} with ingredients: {ingredients}")
            if not contains_allergen_ingredients(ingredients, selected_allergens, allergen_mapping):
                allergen_free_recommendations.append(rec)
        else:
            print(f"Warning: No ingredients found for index {food_index}")

    unique_recommendations = pd.Series(allergen_free_recommendations).value_counts().index.tolist()

    return unique_recommendations[:top_n]

def add_to_favorites(collection, username, food_title, food_index):
    """Add a food item to the user's favorites in MongoDB with the index."""
    # Find the user by username and add the food title along with the index to the favorites list
    food_index = int(food_index)
    collection.update_one(
        {"username": username},
        {"$addToSet": {"favorites": {"title": food_title, "index": food_index}}}  # $addToSet ensures no duplicates
    )