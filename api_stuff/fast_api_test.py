from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel

# # Load the model
# spam_clf = load(open('./models/spam_detector_model.pkl','rb'))


# Initialize an instance of FastAPI
app = FastAPI()

class Item(BaseModel):
    text_message: str
    another_field: str

# Define the default route 
@app.get("/")
def root():
	return {"message": "Welcome to Your Sentiment Classification FastAPI"}


# Define the route to the sentiment predictor
@app.post("/predict_sentiment")
def predict_sentiment(results: Item):

	# polarity = ""

	# if(not(text_message)):
	#     raise HTTPException(status_code=400, 
	#                         detail = "Please Provide a valid text message")

	# prediction = spam_clf.predict(vectorizer.transform([text_message]))

	# if(prediction[0] == 0):
	#     polarity = "Ham"

	# elif(prediction[0] == 1):
	#     polarity = "Spam"
	
	polarity = "Spam"

	return results