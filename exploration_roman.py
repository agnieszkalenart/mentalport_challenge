import pandas as pd


path_roman = "C:\\Users\\roman\\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\"
exerciseResults = pd.read_csv(path_roman + "exerciseResults" + ".csv")

#%%
users = pd.read_csv(path_roman + "users" + ".csv")

#%%
users.describe()


#%%
weeklyExerciseLists = pd.read_csv(path_roman + "weeklyExerciseLists" + ".csv")
weeklyExerciseLists.info()
# function that counts

#%%
exerciseResults = pd.read_csv(path_roman + "exerciseResults" + ".csv")

#%%
exercises = pd.read_csv(path_roman + "exercises" + ".csv")


#%%
psychologicalAreas = pd.read_csv(path_roman + "psychologicalAreas" + ".csv")

#%%
routineItems = pd.read_csv(path_roman + "routineItems" + ".csv")


#%%
scheduledExercises = pd.read_csv(path_roman + "scheduledExercises" + ".csv")



#%%
# import a json dataset
