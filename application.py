import streamlit as st
import pandas as pd
import data_access as da
import base64
import io
import gspread

# Player Name
# Player ID
# Season
# Date of Injury
# Date of Injury Resolved
# Season Window
# Type Of Injury
# Area of Injury
# Side of Injury
# Contact Injury
# Days Missed
# Games Missed
# Description

st.set_page_config(layout="wide")


@st.cache(allow_output_mutation=True)
def get_data():
    return []


player_options = da.player_data()
injury_options = da.injury_options_data()

title = st.header("Player Injury Input Tool")

password = st.text_input(
    label="Password (Remember to clear when done)", type="password"
)

if password == st.secrets["password"]:
    l_column, m_column, r_column = st.columns((1, 1, 1))

    players = l_column.selectbox(
        label="Players", options=player_options["Player"].dropna(), index=0
    )

    # player_id = m_column.subheader(
    #     "Player ID: "
    #     + str(player_options[player_options["Player"] == players].loc[0, "Player ID"])
    # )

    season = m_column.selectbox(
        label="Season", options=injury_options["Season"].dropna(), index=2
    )

    date_of_injury = r_column.date_input(label="Date of Injury")

    date_of_recovery = l_column.date_input(label="Date of Recovery")

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
        last_row = len(da.injury_tracker()["Player Name"]) + 2
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
    st.write(show_dataframe)

    csv = pd.DataFrame(get_data()).to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko = f'<a href="data:file/csv;base64,{b64}" download="exercises.csv">Download csv file</a>'
    st.markdown(linko, unsafe_allow_html=True)
