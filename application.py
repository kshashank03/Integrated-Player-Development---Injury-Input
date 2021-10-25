import streamlit as st
import pandas as pd
import data_access as da
# import base64
# import io
import gspread
from datetime import datetime

st.set_page_config(layout="wide")


@st.cache(allow_output_mutation=True)
def get_data():
    return []


player_options = da.player_data()
injury_options = da.injury_options_data()
injury_data = da.injury_tracker()

title = st.header("Player Injury Input Tool")

password = st.text_input(
    label="Password (Remember to clear when done)", type="password"
)

if password == st.secrets["password"]:
    l_column, m_column, r_column = st.columns((1, 1, 1))

    players = l_column.selectbox(
        label="Players", options=player_options["Player"].dropna(), index=0
    )

    season = m_column.selectbox(
        label="Season", options=injury_options["Season"].dropna(), index=2
    )

    date_of_injury = r_column.date_input(label="Date of Injury")

    date_of_recovery = l_column.date_input(label="Date of Recovery", value=None) # This isn't working

    season_window = m_column.selectbox(
        label="Season Window", options=injury_options["Season Window"].dropna(), index=0
    )

    type_of_injury = r_column.selectbox(
        label="Type of Injury",
        options=injury_options["Type Of Injury"].dropna(),
        index=0,
    )

    area_of_injury = l_column.selectbox(
        label="Area of Injury",
        options=injury_options["Area of Injury"].dropna(),
        index=0,
    )

    side_of_injury = m_column.selectbox(
        label="Side of Injury",
        options=injury_options["Side of Injury"].dropna(),
        index=0,
    )

    contact_injury = m_column.selectbox(
        label="Contact Injury",
        options=injury_options["Contact Injury"].dropna(),
        index=0,
    )
    # print(exercise_groups)
    days_missed = r_column.number_input(label="Days Missed", step=1)
    games_missed = l_column.number_input(label="Games Missed", step=1)

    description = m_column.text_area(label="Description")

    player_id = str(
        player_options[player_options["Player"] == players]
        .reset_index()
        .loc[0, "Player ID"]
    )

    if st.button(label="Add Row"):
        get_data().append(
            {
                "Player Name": players,
                "Player ID": player_id,
                "Season": season,
                "Date of Injury": date_of_injury,
                "Date of Injury Resolved": date_of_recovery,
                "Season Window": season_window,
                "Type of Injury": type_of_injury,
                "Area of Injury": area_of_injury,
                "Side of Injury": side_of_injury,
                "Contact Injury": contact_injury,
                "Days Missed": days_missed,
                "Games Missed": games_missed,
                "Description": description,
            }
        )

    if st.button(label="Clear Table"):
        get_data().clear()

    if st.button(label="Clear Last Row"):
        get_data().pop()

    if st.button(label="Append to Google Doc"):
        last_row = len(injury_data.iloc[:, 0]) + 2
        number_rows_to_add = len(pd.DataFrame(get_data())) + last_row
        temp_dataframe = pd.DataFrame(get_data())
        temp_dataframe["Date of Injury"] = pd.to_datetime(
            temp_dataframe["Date of Injury"]
        )
        temp_dataframe["Date of Injury Resolved"] = pd.to_datetime(
            temp_dataframe["Date of Injury Resolved"]
        )
        temp_dataframe["Date of Injury"] = temp_dataframe["Date of Injury"].dt.strftime(
            "%d-%m-%Y"
        )
        temp_dataframe["Date of Injury Resolved"] = temp_dataframe[
            "Date of Injury Resolved"
        ].dt.strftime("%d-%m-%Y")
        temp_dataframe = temp_dataframe.astype(str)
        values_to_append = temp_dataframe.values.tolist()
        gc = gspread.service_account_from_dict(da.sa_creds)

        sh = gc.open_by_key(
            "1KIVZXn4xPl-ewEThJVAPlX2mexZCucVOydULgqhhEJ8"
        )  # Injury Data

        sh.worksheet("InjuryTrackingLive").update(
            f"A{last_row}:M{number_rows_to_add}", values_to_append
        )

    show_dataframe = pd.DataFrame(get_data())
    if len(show_dataframe) < 1:
        pass 
    else:
        show_dataframe["Date of Injury"] = pd.to_datetime(show_dataframe["Date of Injury"])
        show_dataframe["Date of Injury Resolved"] = pd.to_datetime(
            show_dataframe["Date of Injury Resolved"]
        )
        show_dataframe["Date of Injury"] = show_dataframe["Date of Injury"].dt.strftime(
            "%d-%m-%Y"
        )
        show_dataframe["Date of Injury Resolved"] = show_dataframe[
            "Date of Injury Resolved"
        ].dt.strftime("%d-%m-%Y")
    
    

    st.header("Data to Append")
    st.caption("This is the data you'll be appending to the Google Sheet")
    st.write(show_dataframe)
    st.header("Current Player Data")
    st.caption("Displays records on the Google Sheet for the player you selected in the dropdown at the top of the screen")
    current_player_data = injury_data[injury_data["Player Name"] == players]
    if len(current_player_data.index) == 0:
        pass
    else:
        update_radio_options = [option for option in current_player_data.index]
        update_radio = st.radio("Which row to update", update_radio_options)
    current_player_dataframe = st.write(current_player_data)

    # l_column, m_column, r_column = st.columns((1, 1, 1))

    if len(current_player_data.index) == 0:
        pass
    else:
        # update_players = l_column.selectbox(
        #     label="Players", options=player_options["Player"].dropna(), index=0
        # )

        # update_season = m_column.selectbox(
        #     label="Season", options=injury_options["Season"].dropna(), index=2
        # )

        # update_date_of_injury = r_column.date_input(label="Date of Injury")

        values_to_update = injury_data.iloc[update_radio, :]

        update_date_of_recovery = st.date_input(label="Date of Recovery", value=pd.to_datetime(values_to_update["Date of Injury Resolved"]), key="update_date_of_recovery") # This isn't working


        update_season_window_options = injury_options["Season Window"].dropna()
        update_season_window_options_index = update_season_window_options[update_season_window_options==values_to_update["Season Window"]].index[0]

        update_season_window = st.selectbox(
            label="Season Window", options=update_season_window_options, index=int(update_season_window_options_index)
        , key="update_season_window")


        update_type_of_injury_options = injury_options["Type Of Injury"].dropna()
        update_type_of_injury_options_index = update_type_of_injury_options[update_type_of_injury_options==values_to_update["Type Of Injury"]].index[0]
        update_type_of_injury = st.selectbox(
            label="Type of Injury",
            options=update_type_of_injury_options,
            index=int(update_type_of_injury_options_index), key="update_type_of_injury"
        )


        update_area_of_injury_options = injury_options["Area of Injury"].dropna()
        update_area_of_injury_options_index = update_area_of_injury_options[update_area_of_injury_options==values_to_update["Area of Injury"]].index[0]
        update_area_of_injury = st.selectbox(
            label="Area of Injury",
            options=update_area_of_injury_options,
            index=int(update_area_of_injury_options_index), key="update_area_of_injury"
        )


        update_side_of_injury_options = injury_options["Side of Injury"].dropna()
        update_side_of_injury_options_index = update_side_of_injury_options[update_side_of_injury_options==values_to_update["Side of Injury"]].index[0]
        update_side_of_injury = st.selectbox(
            label="Side of Injury",
            options=update_side_of_injury_options,
            index=int(update_side_of_injury_options_index), key="update_side_of_injury"
        )

        # update_contact_injury = m_column.selectbox(
        #     label="Contact Injury",
        #     options=injury_options["Contact Injury"].dropna(),
        #     value=values_to_update["Contact Injury"]
        # )
        update_days_missed = st.number_input(label="Days Missed", step=1, value=values_to_update["Days Missed"], key="update_days_missed")
        update_games_missed = st.number_input(label="Games Missed", step=1, value=values_to_update["Games Missed"], key="update_games_missed")

        update_description = st.text_area(label="Description", value=values_to_update["Description"], key="update_description")

        if st.button(label="Update This Row of Data"):
            index_value = str(update_radio + 2)
            worksheet = da.injury_tracker_worksheet_object()
            worksheet.update("E" + index_value, update_date_of_recovery.strftime("%d-%m-%Y"))
            worksheet.update("F" + index_value, update_season_window)
            worksheet.update("G" + index_value, update_type_of_injury)
            worksheet.update("H" + index_value, update_area_of_injury)
            worksheet.update("I" + index_value, update_side_of_injury)
            worksheet.update("K" + index_value, update_days_missed)
            worksheet.update("L" + index_value, update_games_missed)
            worksheet.update("M" + index_value, update_description)