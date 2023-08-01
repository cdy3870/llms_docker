import streamlit as st
import requests
import json
import numpy as np

# text_input = st.text_input("Enter some text")
# cand_labels = st.text_input("Candidate labels")



# # Get a prediction
# # sequence_to_classify = "one day I will see the world"
# # candidate_labels = ['travel', 'cooking', 'dancing']
# # labels = cand_labels.split(" ")

# inputs = {"text_input": text_input, "candidate_labels": cand_labels}

# if st.button("Get most likely label"):
# 	res = requests.post(url="http://0.0.0.0:8000/predict_sentiment", json=inputs)
# 	predictions = json.loads(res.text)
# 	sequence = predictions["labels"][np.argmax(predictions["scores"])]

# 	st.subheader(f"{sequence}")





doi = st.text_input("Enter a research topic (ex. machine learning and drones) for related papers")
inputs = {"text": doi}

if st.button("Get recommended papers"):
	res = requests.post(url="http://0.0.0.0:8000/get_recs", json=inputs)
	st.markdown(res.text)	

doi = st.text_input("Enter an arxiv DOI or paper name")
inputs = {"text": doi}

if st.button("Get info"):
	# res = requests.post(url="http://0.0.0.0:8000/get_summary", json=inputs)
	# st.markdown(f"Summary: {res.text}")

	res = requests.post(url="http://0.0.0.0:8000/get_con", json=inputs)

	bullet_points = res.text.split("\\n-")
	print(bullet_points)

	st.markdown(f"Contributions:")
	for i, bullet in enumerate(bullet_points[1:]):
		st.markdown(f"{i + 1}:{bullet}")

	res = requests.post(url="http://0.0.0.0:8000/get_details", json=inputs)
	st.markdown(res.text)