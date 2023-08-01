from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel
# from transformers import pipeline
import json
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType

# classifier = pipeline("zero-shot-classification",
#                       model="facebook/bart-large-mnli")

key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=key)
tools = load_tools(
	["arxiv"],
)

agent_chain = initialize_agent(tools, llm, 
								agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Initialize an instance of FastAPI
app = FastAPI()


# Define the default route 
@app.get("/")
def root():
	return {"message": "Welcome to Your Sentiment Classification FastAPI"}


class Item(BaseModel):
    text_input: str
    candidate_labels: str

# Define the route to the sentiment predictor
@app.post("/predict_sentiment")
def predict_sentiment(item: Item):
	labels = item.candidate_labels.split(" ")
	prediction = classifier(item.text_input, labels)


	# polarity = ""

	# if(not(text_message)):
	#     raise HTTPException(status_code=400, 
	#                         detail = "Please Provide a valid text message")

	# prediction = spam_clf.predict(vectorizer.transform([text_message]))

	# if(prediction[0] == 0):
	#     polarity = "Ham"

	# elif(prediction[0] == 1):
	#     polarity = "Spam"

	return prediction


class DOI(BaseModel):
    text: str

@app.post("/get_summary")
def get_summary(doi: DOI):
	response = agent_chain.run(f"What is the paper {doi.text} about?")

	print(response)

	return response

@app.post("/get_con")
def get_con(doi: DOI):
	response = agent_chain.run(f"What are the main contributions of {doi.text} as a bullet points?")

	print(response)

	return response

@app.post("/get_details")
def get_details(doi: DOI):
	response = agent_chain.run(f"What year was {doi.text} published and in what conference or journal?")

	print(response)

	return response

@app.post("/get_recs")
def get_recs(topic: DOI):
	response = agent_chain.run(f"Can you find a list of papers related to {topic}")

	print(response)

	return response



