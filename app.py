import requests
import streamlit as st

st.write("HELLO")

headers = {
    "authorization": st.secrets["auth_key"],
    "content-type": "application/json"
}