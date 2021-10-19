import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import data_access as da

background_color = "rgb(246,246,246)"

dropdown_width = "60%"

# Data
calendar_data = da.calendar_schedule()
calendar_data["Date"] = pd.to_datetime(calendar_data["Date"], dayfirst=True)

exercise_data = da.exercise_database()

daily_workout_card = da.daily_workout_card()

total_calendar_data = da.overall_calendar_database()
total_calendar_data["Date"] = pd.to_datetime(
    total_calendar_data["Date"], dayfirst=True)

data_option = da.data_options()
##

calendar_data["Date"] = pd.to_datetime(calendar_data["Date"], dayfirst=True)

def blank_dashtable():
    records = {"player_name":['player_name'], 
            "date_picker":['date_picker'], 
            "block":['block'], 
            "exercise":["exercise"],
            "set":['set'], 
            "rep":['rep'],
            "time":['time'],
            "weight":['weight'],
            "tempo":['tempo'], 
            "strength":['strength'],
            "notes":['notes'], 
            "contraction_types":['contraction_types'],
            "time_of_day":['time_of_day']
            }
    
    data = pd.DataFrame(records)
    
    table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in data.columns],
                data=data.to_dict('records'))
    
    return table

def player_name():

    player_name_options = daily_workout_card["Player Name"].dropna().unique()
    first_name = player_name_options[0]

    options = []
    for i in player_name_options:
        options.append({'label': i, 'value': i})

    name_dropdown = dcc.Dropdown(
        options=options, value=first_name, id="player-name-dropdown", style={"width": dropdown_width,  })

    return name_dropdown


def initial_exercise_check():

    different_groupings = exercise_data["PrimaryGroups"].dropna().unique()

    individual_exercises = []
    for i in different_groupings:
        for x in i.split("-"):
            if x not in individual_exercises:
                individual_exercises.append(x)

    exercise_options = []

    for i in individual_exercises:
        exercise_options.append({'label': i, 'value': i})

    initial_exercise_dose_dropdown = dcc.Dropdown(
        options=exercise_options, multi=True, placeholder="Exercise Group", id="exercise-dose-dropdown", style={"width": dropdown_width,  })

    return initial_exercise_dose_dropdown


def exercise_dropdown(primary_group_list):
    if primary_group_list != None:
        filtered_data = exercise_data
        filtered_data = filtered_data[filtered_data["PrimaryGroups"].notna()]
        for i in primary_group_list:
            filtered_data = filtered_data[filtered_data["PrimaryGroups"].str.contains(i)]

        exercise_options = []
        options = filtered_data["ExerciseName"].dropna()
        for i in options:
            exercise_options.append({'label': i, 'value': i})
        
        exercise_dropdown = dcc.Dropdown(
            options=exercise_options, multi=False, placeholder="Exercise", id="exercise-dropdown", style={"width": dropdown_width,  })

        return exercise_dropdown

    else:
        exercise_options = []
        options = exercise_data["ExerciseName"].dropna()
        for i in options:
            exercise_options.append({'label': i, 'value': i})
        
        exercise_dropdown = dcc.Dropdown(
            options=exercise_options, multi=False, placeholder="Exercise", id="exercise-dropdown", style={"width": dropdown_width,  })

        return exercise_dropdown

def date_picker():
    date_value = dcc.DatePickerSingle(
        id='date-picker',
        display_format="DD-MM-YYYY",
        placeholder="Date"
         )
    return date_value

def block_count():
    options = []
    for i in data_option["Block"].dropna():
        options.append({'label': i, 'value': i})

    block_dropdown = dcc.Dropdown(
        options=options, placeholder="Blocks", id="block-dropdown", style={"width": dropdown_width,  })

    return block_dropdown

def set_count():
    options = []
    for i in data_option["Sets"].dropna():
        options.append({'label': i, 'value': i})

    set_dropdown = dcc.Dropdown(
        options=options, placeholder="Sets", id="set-dropdown", style={"width": dropdown_width,  })

    return set_dropdown

def rep_count():
    options = []
    for i in data_option["Reps"].dropna():
        options.append({'label': i, 'value': i})

    rep_dropdown = dcc.Dropdown(
        options=options, placeholder="Reps", id="rep-dropdown", style={"width": dropdown_width,  })

    return rep_dropdown

def time_input_text_area():
    options = []
    for i in data_option["Time"].dropna():
        options.append({'label': i, 'value': i})
    time_dropdown = dcc.Dropdown(
        options=options, placeholder="Time", id="time-input-dropdown", style={"width": dropdown_width,  })

    return time_dropdown


def weight_input_text_area():
    options = []
    for i in data_option["Weight"].dropna():
        options.append({'label': i, 'value': i})

    # weight_dropdown = dcc.Dropdown( # He wanted this changed
    #     options=options, placeholder="Weight", id="weight-dropdown", style={"width": dropdown_width,  })

    weight_dropdown = dcc.Textarea(
            id='weight-dropdown',
            placeholder="Weight",
            )

    return weight_dropdown
    
def tempo_input_text_area():
    options = []
    for i in data_option["Tempo"].dropna():
        options.append({'label': i, 'value': i})

    tempo_dropdown = dcc.Dropdown(
        options=options, placeholder="Tempo", id="tempo-dropdown", style={"width": dropdown_width,  })

    return tempo_dropdown

def strength_goal_dropdown():
    options = []
    for i in data_option["Strength Goal"].dropna():
        options.append({'label': i, 'value': i})

    strength_dropdown = dcc.Dropdown(
        options=options, placeholder="Strength Goal", id="strength-dropdown", style={"width": dropdown_width,  })

    return strength_dropdown

def notes_text_area():
    notes_input = dcc.Textarea(
            id='notes-area',
            placeholder="Notes",
            )
    
    return notes_input

def exercise_type():
    exercise_types = ["CM", "LB"]
    options = []
    for i in exercise_types:
        options.append({'label': i, 'value': i})

    exercise_types_dropdown = dcc.Dropdown(
        options=options, placeholder="Exercise Type", id="exercise-types-dropdown", style={"width": dropdown_width,  })

    return exercise_types_dropdown


def contraction_type_dropdown():
    options = []
    for i in data_option["Contraction Type"].dropna():
        options.append({'label': i, 'value': i})

    contraction_types_dropdown = dcc.Dropdown(
        options=options, placeholder="Contraction Type", id="contraction-types-dropdown", style={"width": dropdown_width,  })

    return contraction_types_dropdown

def include_type_dropdown():
    options = []
    for i in data_option["Include"].dropna():
        options.append({'label': i, 'value': i})

    include_types_dropdown = dcc.Dropdown(
        options=options, placeholder="Include Type", id="include-types-dropdown", style={"width": dropdown_width,  })

    return include_types_dropdown

def contraction_speed_dropdown():
    options = []
    for i in data_option["Contraction Speed"].dropna():
        options.append({'label': i, 'value': i})

    contraction_speed_dropdown = dcc.Dropdown(
        options=options, placeholder="Contraction Speed", id="contraction-speed-dropdown", style={"width": dropdown_width,  })

    return contraction_speed_dropdown

def time_dropdown_():
    options = []
    for i in data_option["Time Of Day"].dropna():
        options.append({'label': i, 'value': i})

    time_dropdown = dcc.Dropdown(
        options=options, placeholder="Time of Day", id="time-of-day-dropdown", style={"width": dropdown_width,  })

    return time_dropdown

