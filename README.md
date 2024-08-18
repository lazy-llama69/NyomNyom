<p align="center">
	<h2 align="center"> NYOM NYOM</h2>
	<h4 align="center"> Machine Learning Food Recommendation Web App
This web application offers a comprehensive and personalized food recommendation experience, enhanced by a rich set of features designed to help users discover and enjoy new dishes.

<h4>
</p>

---
## Preview
- [NYOM NYOM](https://nyomnyom.streamlit.app)
## Functionalities
- User Authentication: Secure login and sign-up with MongoDB Atlas Cloud Database storing user information, including passwords and favorite meals.
- Database Operations: Add, modify, and delete information within the database.
- Meal Database Search: Search through a dataset of 13,000 meals with filters for allergens, and cuisines.
- Advanced Search Capabilities: Search for meals by title or ingredients.
- Personalized Recommendations: 9 food items recommended based on the user’s favorite meals using a TF-IDF matrix and item-based collaborative filtering.
- Meal Information Display: View detailed meal information, including an image, title, ingredients, and cooking instructions.
- Favorites Management: Add meals to favorites, view them in a dedicated tab, and remove them as desired.
- Recommendation System Based on Favorites: Tailored recommendations based on the user’s favorite meals.
- Random Food Generator: Discover meals randomly, either based on selected ingredients or completely at random.
- Go Crazy Feature: Generate a unique meal using randomly selected ingredients, with AI-generated image, title, ingredients list, and cooking instructions using Gemini and Hugging Face APIs.

<br>


## Instructions to run

* Pre-requisites:
	-  pandas==2.2.2
	-  Pillow==10.4.0
	-  pymongo==4.8.0
	-  Requests==2.32.3
	-  scikit_learn==1.5.1
	-  streamlit==1.37.1
	-  google-generativeai

* Install all pre-requisites 
(ensure you are in the deploy folder before running this line of command): 
```bash
$ pip install -r requirements.txt
```
* If any errors pop up during installation, just pip install one by one.
* Executing the source file
```bash
$ streamlit run login.py
```

## Contributors

<table>
<tr align="center">


<td>

Chang Yi Qian

<p align="center">

</p>
<p align="center">
<a href = "https://github.com/yiqianeee"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/yi-qian-chang-048420228/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>


<td>

Tang Jia Shen
<p align="center">

</p>
<p align="center">
<a href = "https://github.com/lazy-llama69"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/jia-shen-tang-b1a564170/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>



<td>

Gavin Pan

<p align="center">
</p>
<p align="center">
<a href = "https://www.linkedin.com/in/gavpan/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>
</tr>
  </table>
  
## Acknowledgments

- This project utilizes the [Gemini API](https://ai.google.dev/api?lang=python) for generating unique meal titles and instructions. Special thanks to the teams behind these tools for the open source API. 
- The image generation feature uses the [Stable Diffusion v1-5 model](https://huggingface.co/runwayml/stable-diffusion-v1-5) provided by Hugging Face. We thank them for offering such a comprehensive model that enhances the visual experience of this application.
- The food dataset used in this project is the [Food Ingredients and Recipes Dataset with Images](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images) by Sakshi Goel, sourced from the Epicurious website. This dataset contains 13k images and rows, providing a robust foundation for meal recommendations and search functionality.

## Important Note

**Please be aware** that this project contains sensitive API keys for the following services:

- **Gemini API**: Used for generating meal titles and instructions.
- **Hugging Face API**: Used for generating meal images via the Stable Diffusion model.
- **MongoDB Atlas**: Used for storing user information, including passwords and favorite meals.

These keys are integral to the functioning of the application. **However, they should not be used for any purposes outside of this project.** Unauthorized use or abuse of these keys could lead to security risks, financial costs, or the disabling of the API access.

If you fork or clone this repository, **please ensure to replace the API keys with your own,** or remove them entirely if not needed. 

**Responsible usage of these resources is highly encouraged.**


## License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

<p align="center">
	Made with pure blood, sweat, tears, and :heart: </a>
</p>


