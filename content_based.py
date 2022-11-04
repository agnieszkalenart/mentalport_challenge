"""
File for creating the content-based user-item matrix
"""

# standard library imports

# 3rd party imports
import pandas as pd
import re
import scipy.spatial

# local imports (i.e. our own code)
from helper import get_user_users

# import datasets
psy = pd.read_csv('mp_data-main/mp_data/psychologicalAreas.csv')
exercises=pd.read_csv("mp_data-main/mp_data/exercise-original-fixed.csv")

# extract user_ids from psychological areas dataframe
psy["users"] = get_user_users(psy)

# make columns for each psychological area
users_kw = psy[["psychologicalAreas", "users"]].rename(columns = {"users" : "user_id"})
users_kw = users_kw.set_index("user_id").psychologicalAreas.apply(lambda x: x.replace('[', '').replace(']', '')).str.get_dummies(',').reset_index()

# drop duplicate users
users_kw = users_kw.reset_index()
users_kw = users_kw.drop_duplicates(subset = 'user_id')
users_kw.set_index('user_id', inplace = True)
users_kw = users_kw[['burnout', 'confidence', 'depression', 'discipline', 'meaning', 'motivation', 'relationships', 'stress']]

# transform exercises dataframe
exercises = exercises.replace(to_replace="ja", value= 1)
exercises = exercises.replace(to_replace="nein", value = 0)
exercises = exercises[['Bez.','Sinnfindung', 'Burnout', 'Depression', 'Selbstbwusstsein','Beziehungsberatung', 'Selbstdisziplin', 'Motivation','Stressmanagement']].dropna(subset='Bez.')
exercises = exercises.rename(columns = {'Bez.':'exercise_id','Burnout' : 'burnout', 'Selbstbwusstsein':'confidence', 'Depression':'depression', 'Selbstdisziplin':'discipline','Sinnfindung':'meaning','Motivation':'motivation', 'Beziehungsberatung':'relationships', 'Stressmanagement':'stress'})
ex_kw = exercises[['exercise_id', 'burnout', 'confidence', 'depression', 'discipline', 'meaning', 'motivation', 'relationships', 'stress']]
ex_kw.set_index('exercise_id', inplace = True)

# generate final user-item distance matrix using jaccard distance.
jaccard = scipy.spatial.distance.cdist(users_kw, ex_kw, 
                                       metric='jaccard')
user_distance = 1 - pd.DataFrame(jaccard, columns=ex_kw.index.values,  index=users_kw.index.values)

# save result as csv
user_distance.to_csv('mp_data-main/out/content_based.csv')




