import gspread
import pandas as pd
import numpy as np
import streamlit as st
import json

sa_creds = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
}


def player_data():
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key("1kP1QUYDOs30xSqrlbEWVvCjXPVjQ2zRUTS_OuhSQkuQ")  # Player Data

    dataframe = pd.DataFrame(sh.sheet1.get_all_records())
    dataframe = dataframe.replace("", np.nan)

    return dataframe


def injury_options_data():
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key("1KIVZXn4xPl-ewEThJVAPlX2mexZCucVOydULgqhhEJ8")  # Injury Data

    dataframe = pd.DataFrame(sh.worksheet("InjuryOptions").get_all_records())
    dataframe = dataframe.replace("", np.nan)

    return dataframe


def injury_tracker():
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key("1KIVZXn4xPl-ewEThJVAPlX2mexZCucVOydULgqhhEJ8")  # Injury Data

    dataframe = pd.DataFrame(sh.worksheet("InjuryTrackingLive").get_all_records())
    dataframe = dataframe.replace("", np.nan)

    return dataframe

def injury_tracker_worksheet_object():
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key("1KIVZXn4xPl-ewEThJVAPlX2mexZCucVOydULgqhhEJ8").worksheet("InjuryTrackingLive")  # Injury Data

    return sh


def calendar_schedule():
    # gc = gspread.service_account(filename="credentials.json")
    # gc = gspread.service_account(filename=creds_dict,)
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key(
        "10SdQhvm7ndVYgmZkSqvCm-VCzCNu0yM7sRgrst8nWKc"
    )  # Calendar Schedule Database

    dataframe = pd.DataFrame(sh.sheet1.get_all_records())
    dataframe = dataframe.replace("", np.nan)

    return dataframe


def exercise_database():
    # gc = gspread.service_account(filename="credentials.json")
    # gc = gspread.service_account(filename=creds_dict)
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key(
        "1iPEXaR9HXw817QJ_RNzZEE7qCtOKjVfJ-vPuiU-RpHI"
    )  # Calendar Schedule Database

    dataframe = pd.DataFrame(sh.worksheet("ExerciseDatabaseLive").get_all_records())
    dataframe = dataframe.replace("", np.nan)

    return dataframe


def daily_workout_card():
    # gc = gspread.service_account(filename="credentials.json")
    # gc = gspread.service_account(filename=creds_dict)
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key(
        "1iPEXaR9HXw817QJ_RNzZEE7qCtOKjVfJ-vPuiU-RpHI"
    )  # Calendar Schedule Database

    dataframe = pd.DataFrame(sh.worksheet("DailyWorkoutCardLive").get_all_records())
    dataframe = dataframe.replace("", np.nan)

    return dataframe


def overall_calendar_database():
    # gc = gspread.service_account(filename="credentials.json")
    # gc = gspread.service_account(filename=st.secrets["credentials"])
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key("10SdQhvm7ndVYgmZkSqvCm-VCzCNu0yM7sRgrst8nWKc")

    dataframe_import = pd.DataFrame(sh.worksheet("Total Activity").get_all_records())
    dataframe = dataframe_import.replace("", np.nan)

    return dataframe


def data_options():
    # gc = gspread.service_account(filename="credentials.json")
    # gc = gspread.service_account(filename=creds_dict)
    gc = gspread.service_account_from_dict(sa_creds)

    sh = gc.open_by_key("1iPEXaR9HXw817QJ_RNzZEE7qCtOKjVfJ-vPuiU-RpHI")

    dataframe_import = pd.DataFrame(sh.worksheet("ListsLive").get_all_records())
    dataframe = dataframe_import.replace("", np.nan)

    return dataframe
