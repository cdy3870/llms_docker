import streamlit as st
import requests
import json

inputs = {"text_message": "test", "another_field": "test2"}

if st.button("Run test"):
	print(inputs)
	res = requests.post(url="http://api/predict_sentiment", json=inputs)
	st.subheader(f"{res.text}")