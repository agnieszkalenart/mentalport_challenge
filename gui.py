# standard library imports
from tkinter import *
from tkinter import messagebox
# 3rd party imports
import customtkinter
import pandas as pd
#from happytransformer import HappyTextClassification

# local imports (i.e. our own code)
from test import filter

root = customtkinter.CTk()

root.title('Mentalport GUI for Data Input')

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
root.geometry("1200x700")
root.configure(bg='black')


exercises = []
needs = []

model_data = pd.DataFrame(columns = ['ex_col', 'score_col'])
model_data['ex_col'] = exercises['Bez.']
model_data['score_col'] = [1 for i in range(len(model_data))]



def evaluate_mood(mood_text):
    pass
    '''
    model = HappyTextClassification(
    model_type="DISTILBERT",
    model_name="distilbert-base-uncased-finetuned-sst-2-english",
    )
    result = model.classify_text(mood_text)

    if result.label == "POSITIVE":
        print("Positive")
    else:
        print("Negative")
    '''

def add_to_exercises_and_needs():
    if exercise_combobox.get() != '' and need_combobox.get() != '':
        exercises.append(exercise_combobox.get())
        needs.append(need_combobox.get())
        exercise_combobox.set('')
        need_combobox.set('')
        exercises_added_label.configure(text=f"Exercises: {exercises}")
        needs_added_label.configure(text=f"Needs: {needs}")
    elif exercise_combobox.get() != '':
        exercises.append(exercise_combobox.get())
        exercise_combobox.set('')
        exercises_added_label.configure(text=f"Exercises: {exercises}")
    elif need_combobox.get() != '':
        needs.append(need_combobox.get())
        need_combobox.set('')
        needs_added_label.configure(text=f"Needs: {needs}")
    else:
        messagebox.showinfo(title='Info', message='Please select some exercises and needs.')

def reset_exercises_and_needs():
    global exercises
    global needs
    exercises = []
    needs = []
    exercises_added_label.configure(text=f"Exercises: {exercises}")
    needs_added_label.configure(text=f"Needs: {needs}")


def get_output():
    '''
    if feeling_entry.get() != '':
        mood = evaluate_mood(feeling_entry.get())
    if id_entry.get() == '':    
        model_recommendation = recommendation(user_id=None, input_time=int(time_combobox.get()))    
    else:
        model_recommendation = recommendation(user_id=id_entry.get(), input_time=int(time_combobox.get()))    
    '''    
    exercise_recommendation = []
    exercise_indexes = filter(model_data, exercises, 10, 'meditation', 'ex_col', 'score_col')
    for i in exercise_indexes:
        exercise_recommendation.append(exercises[exercises['Bez.'] == i]['Titel'])
    output_label.configure(text=f"User-based content: {exercise_recommendation[0]}\nContent-based content: {exercise_recommendation[1]}\nKnowledge-based content: {exercise_recommendation[2]}")
      
frame = customtkinter.CTkFrame(master=root,
                               width=1200,
                               height=700,
                               corner_radius=10,
                               bg='black',
                               fg_color='black',
                               border_width=2, border_color="white")




title_label = customtkinter.CTkLabel(root, text="Mentalport GUI for Data Input", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )


time_label = customtkinter.CTkLabel(root, text="How much time do you want to invest today? Maximum in mins:", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )

time_combobox = customtkinter.CTkOptionMenu(master=root,
                                       values=['5', '10', '20'], 
                                       width=130,
                                        height=40,
                                        fg_color=("#2a9d8f", "#0F3D3E"),
                                        corner_radius=8, 
                                        text_font=('Times New Roman', 24),
                                        bg_color='black',
                                        text_color='white',
                                        
                                        button_color='#0F3D3E',
                                        button_hover_color='#3AB4F2',
                                        dropdown_text_font=('Times New Roman', 24),
                                                           
                                        )

exercise_label = customtkinter.CTkLabel(root, text="How do you want to achieve this? Type of exercise: ", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )

exercise_combobox = customtkinter.CTkOptionMenu(master=root,
                                       values=['Thinking', 'Meditating', 'Journaling', 'Being creative', 
                                               'Learning', 'Moving', 'Breathe', 'Being active', 'Visualize'], 
                                       width=130,
                                        height=40,
                                        fg_color=("#2a9d8f", "#0F3D3E"),
                                        corner_radius=8, 
                                        text_font=('Times New Roman', 24),
                                        bg_color='black',
                                        text_color='white',
                                        
                                        button_color='#0F3D3E',
                                        button_hover_color='#3AB4F2',
                                        dropdown_text_font=('Times New Roman', 24),
                                                           
                                        )



add_to_exercises_button = customtkinter.CTkButton(root, width=195,
                                 height=40,
                                 corner_radius=8,
                                 command=add_to_exercises_and_needs,
                                 text="Add to exercises and needs",
                                 fg_color='#2a9d8f',
                                 text_font=('Times New Roman', 24),
                               bg_color='black',
                               hover_color='#3AB4F2',
                               border_width=2, border_color="white",
                               text_color='black'
                                 )

reset_exercises_button = customtkinter.CTkButton(root, width=195,
                                 height=40,
                                 corner_radius=8,
                                 command=reset_exercises_and_needs,
                                 text="Reset exercises and needs",
                                 fg_color='#2a9d8f',
                                 text_font=('Times New Roman', 24),
                               bg_color='black',
                               hover_color='#3AB4F2',
                               border_width=2, border_color="white",
                               text_color='black'
                                 )


need_label = customtkinter.CTkLabel(root, text="what do you need right now?", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )



need_combobox = customtkinter.CTkOptionMenu(master=root,
                                       values=['Energy Boost', 'Motivation', 'Relaxation', 'Fall asleep', 
                                               'Serenity', 'Stress reduction', 'Overcoming (thinking) blockades', 'Positivity - mood boost', 
                                               'fun', 'Self-awareness boost (Strengthening strengths)', 'Self-love', 'pain relief', 'else'], 
                                       width=130,
                                        height=40,
                                        fg_color=("#2a9d8f", "#0F3D3E"),
                                        corner_radius=8, 
                                        text_font=('Times New Roman', 24),
                                        bg_color='black',
                                        text_color='white',
                                        
                                        button_color='#0F3D3E',
                                        button_hover_color='#3AB4F2',
                                        dropdown_text_font=('Times New Roman', 24),
                                                           
                                        )

id_label = customtkinter.CTkLabel(root, text="User ID:", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )

id_entry = customtkinter.CTkEntry(root, width=140,
                               height=40,
                               corner_radius=10,
                              fg_color='#2a9d8f',
                              fg='white',
                              text_font=('Times New Roman', 20),
                              justify=CENTER,
                              bg_color='black',
                              border_width=2, border_color="white",
                              text_color='black'
                            )


exercises_added_label = customtkinter.CTkLabel(root, text=f"Exercises: {exercises}", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )

needs_added_label = customtkinter.CTkLabel(root, text=f"Needs: {needs}", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )

feeling_label = customtkinter.CTkLabel(root, text=f"How do you feel right now? Type here:", width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )



feeling_entry = customtkinter.CTkEntry(root, width=140,
                               height=40,
                               corner_radius=10,
                              fg_color='#2a9d8f',
                              fg='white',
                              text_font=('Times New Roman', 20),
                              justify=CENTER,
                              bg_color='black',
                              border_width=2, border_color="white",
                              text_color='black'
                            )


get_output_button = customtkinter.CTkButton(root, width=195,
                                 height=40,
                                 corner_radius=8,
                                 command=get_output,
                                 text="Get output",
                                 fg_color='#2a9d8f',
                                 text_font=('Times New Roman', 24),
                               bg_color='black',
                               hover_color='#3AB4F2',
                               border_width=2, border_color="white",
                               text_color='black'
                                 )


output_label = customtkinter.CTkLabel(root, 
                            text=f"User-based content: \nContent-based content: \nKnowledge-based content: ", 
                                width=130,
                               height=40,
                               fg_color=("#2a9d8f", "#0F3D3E"),
                               corner_radius=8, 
                               text_font=('Times New Roman', 24),
                               bg_color='black',
                               )


#Packing them on the screen
frame.grid(row=0, column=0, columnspan=6, rowspan=10, sticky='news')

title_label.grid(row=0, column=0, columnspan=6, sticky='ew', padx=10, rowspan=1)

time_label.grid(row=1, column=0, columnspan=3, rowspan=1, sticky='ew', padx=10)
time_combobox.grid(row=1, column=3, columnspan=3, rowspan=1, sticky='ew', padx=10)
time_combobox.set('10')

exercise_label.grid(row=2, column=0, columnspan=3, rowspan=1, sticky='ew', padx=10)
exercise_combobox.grid(row=2, column=3, columnspan=3, rowspan=1, sticky='ew', padx=10)
exercise_combobox.set('')

need_label.grid(row=3, column=0, columnspan=3, sticky='ew', padx=10, rowspan=1) 
need_combobox.grid(row=3, column=3, columnspan=3, sticky='ew', padx=10, rowspan=1)   
need_combobox.set('')

id_label.grid(row=4, column=0, columnspan=3, sticky='ew', padx=10, rowspan=1) 
id_entry.grid(row=4, column=3, columnspan=3, sticky='ew', padx=10, rowspan=1) 

add_to_exercises_button.grid(row=5, column=0, columnspan=3, sticky='ew', padx=10, rowspan=1,)
reset_exercises_button.grid(row=5, column=3, columnspan=3, sticky='ew', padx=10, rowspan=1,)

exercises_added_label.grid(row=6, column=0, columnspan=6, sticky='ew', padx=10, rowspan=1)
needs_added_label.grid(row=7, column=0, columnspan=6, sticky='ew', padx=10, rowspan=1)

feeling_label.grid(row=8, column=0, columnspan=2, sticky='ew', padx=10, rowspan=1)
feeling_entry.grid(row=8, column=2, columnspan=4, sticky='ew', padx=10, rowspan=1)


get_output_button.grid(row=9, column=0, columnspan=2, sticky='nsew', padx=10, rowspan=3, pady=10)
output_label.grid(row=9, column=2, columnspan=4, sticky='nsew', padx=10, rowspan=3, pady=10)


root.mainloop()
