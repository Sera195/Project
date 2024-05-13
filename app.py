import requests
import streamlit as st

st.write("HELLO, im asdlfkj")

headers = {
    "authorization": st.secrets["auth_token"],
    "content-type": "application/json"
}