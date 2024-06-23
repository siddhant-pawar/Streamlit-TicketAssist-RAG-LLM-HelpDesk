import streamlit as st
import dashoard 
import requests
import json


def home_admin():
    dashoard.Dashboard()  


def fetch_joke(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            joke_data = response.json()
            return joke_data.get("setup", "Unknown setup"), joke_data.get("punchline", "Unknown punchline")
        else:
            return "Failed to fetch joke", ""
    except requests.exceptions.RequestException as e:
        return "Error fetching joke", str(e)

joke_url = "https://official-joke-api.appspot.com/random_joke"
setup, punchline = fetch_joke(joke_url)

def home_user():
    st.write("## User section!! today's joke!!")
    st.write(setup)
    st.write(punchline)
