from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel
# from transformers import pipeline
import json
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType, Tool
from langchain.utilities import GoogleSerperAPIWrapper

# classifier = pipeline("zero-shot-classification",
#                       model="facebook/bart-large-mnli")

llm = OpenAI()
arxiv_tools = load_tools(["arxiv"])
arxiv_agent = initialize_agent(arxiv_tools, llm, 
								agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)


google_tools = [
    Tool(
        name="Intermediate Answer",
        func=GoogleSerperAPIWrapper().run,
        description="useful for when you need to ask with search",
    )
]

google_agent = initialize_agent(google_tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH)

# Initialize an instance of FastAPI
app = FastAPI()


# Define the default route 
@app.get("/")
def root():
	return {"message": "arXiv backend"}


# class Item(BaseModel):
#     text_input: str
#     candidate_labels: str


class Item(BaseModel):
    text: str

# @app.post("/get_summary")
# def get_summary(doi: Item):
# 	response = arxiv_agent.run(f"What is the paper {doi.text} about?")

# 	print(response)

# 	return response

# @app.post("/get_con")
# def get_con(doi: Item):
# 	response = arxiv_agent.run(f"What are the main contributions of {doi.text} as a bullet points?")

# 	print(response)

# 	return response

# @app.post("/get_details")
# def get_details(doi: Item):
# 	response = arxiv_agent.run(f"Give the conference of the paper: {doi.text}")

# 	print(response)

# 	return response

@app.post("/get_recs")
def get_recs(topic: Item):
	response = arxiv_agent.run(f"Can you find a list of papers about {topic.text} and have been accepted into a conference as bullet points?")
	print(response)

	return response


@app.post("/get_h5")
def get_h5(conf: Item):
	response = google_agent.run(f"What is the h5 index of the conference {conf.text}?")

	print(response)

	return response

@app.post("/get_im")
def get_im(conf: Item):
	response = google_agent.run(f"What is the impact score of the conference {conf.text}?")

	print(response)

	return response