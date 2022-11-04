# Mentalport Challenge - STADS Datathon 2022

> This repository holds the code that was developed during the STADS Datathon 2022 by Team 10


## Description

The goal of this challenge was to create a recommender system with the help of neural networks that recommends exercises
to users of the Mentalport app. Users can define how much time they have (e.g. 10 min), what kind of exercise they are 
interested in (e.g. meditation, journaling, breathing) and what their purpose is (e.g. falling asleep, energy boost, 
self-love). They then receive a list of the top 3 recommended exercises for them. After doing one of the exercises, 
users can rate it.  Our goal is to increase the user satisfaction with the exercises that are recommended to them.

To achieve our goal we implemented a neural network weighting the predictions of three different recommender systems. 
This results in the hybrid recommendation approach presented here. The three recommender systems are:

1. User based collaborative filtering
2. Item based collaborative filtering
3. Content based filtering

The user-item matrices needed for collaborative filtering are created in the collaborative_filtering.py file, and can be 
found in the data/out directory.
The content based filtering is implemented in the content_based_filtering.py file.
The hybrid recommender system is implemented in the TODO file.


## Participants

### University of Mannheim

* [Agnieszka Lenart](https://github.com/agnieszkalenart) - M.Sc. Data Science
* [Jan-Paul Briem](https://github.com/jpbriem) - M.Sc. Business Informatics
* [Noel Chia](https://github.com/HelloNoel) - M.Sc. Data Science
* [Roman Hess](https://github.com/romanhess98) - M.Sc. Data Science
* [Mariam Arustashvili](https://github.com/marusta) - M.Sc. Data Science

### DHBW Mannheim

* [German Paul](https://github.com/GermanPaul12) - B.Sc. Business Informatics / Data Science


## Contents of this repository

The project directory is organised in the following way:

| Path                      | Role                                         |
|---------------------------|----------------------------------------------|
| `data/`                   | The data used and created in this challenge  |
| `data/mp_data/`           | Data provided for this challenge             |
| `data/out/`               | Data created by our scripts                  |
| `exploration/`             | Some exploratory analyses to collect ideas   | 
| `collaborative_filtering.py/`  | The process of creating the prediction matrices for user- and item-based collaborative filtering |
| `content_based_filtering.py/`  | The process of creating the content based filtering predictions |
| `ensemble.py/`             | The training of the hybrid recommender network |
| `gui.py`                 | The GUI for the recommender system           |
| `helper.py`             | Helper functions used in the scripts         |
| `final_filtering.py`     | The final filtering process                  |
| `sentiment_analysis.py`  | The sentiment analysis of the optional user inputs  |


## Challenge Presentation

Link to the slides:
[Click me to go to Google!](https://www.google.com)

