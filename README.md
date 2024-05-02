# Research Conference Recommender

This repo contains the code that for a research conference recommender. The purpose is to remove the hassle of figuring out which research conference you should submit your work to. 

## Requirements

The "frontend" is done using Streamlit and the backend/REST API is FastAPI. The setup has been simplified using Docker with multiple containers. The containers will be running on an AWS EC2 
instance. Follow the below instructions in the case that the servers are no longer running on AWS.

```
cd llms_docker
docker-compose up
```

Otherwise, you can access the service here: http://3.84.235.58:8501/

## Libraries, Frameworks, APIs, Cloud Services
1. Libraries and Frameworks
- FastAPI
- Streamlit
- Docker
- BeautifulSoup
- HuggingFace
2. APIs
- OpenAI
- arXiv
3. Resources
- https://www.scimagojr.com/ for conference metrics

## How it works and services involved
### Part 1: Recommendation Based on Categories and Subcategories
1. The first part of the recommendation involves using the full list of journals provided by scimagojr
- The R file containing this information (https://github.com/ikashnitsky/sjrdata) is converted into a csv
- The main categories are scraped from the base website
- The entries are preprocessed and cleaned
2. We then use HuggingFace's zero-shot learning NLP model to determine which main category the topic falls under
- Doing this reduces the number of subcategories to search through  when trying to narrow down the subcategory of the topic
3. We apply the same zero-shot technique on the subcategory and obtain the most relevant subcategories to a topic
4. The final step involves filtering the journals based on the predicted subcategories

### Part 2: Recommendations Based on Papers
1. LangChain is a library used to leverage the capabilities of large language models (llms), when OpenAI's llm is paired with a tool, it is capable of reasoning beyond the environment it was 
trained in
- When paired with the arXiv API, an agent can be created to query and reason with a research paper database
- We make a request for papers related to a specific research topic
2. Once we parse the recommended papers, we can extract the arXiv ids by using a web scraping tool called BeautifulSoup
3. After obtaining arXiv ids, we can find the corresponding conference within the page as well
4. The issue with that the conference within the arXiv page is not processed so we may have a string like "Accepted by the ACM Transactions on Intelligent Systems and Technology (TIST)" but we only need "Transactions on Intelligent Systems and Technology" if we want to search correctly on the SJR conference website
- Therefore we use the DaVinci text completion engine to help parse out this conference
5. Then we can make the GET request on the SJR website
- The results may be multiple editions of the conference/journal, so we parse out all of them and get the most recent one
- The h5-index is then extracted 
6. We make our final suggestions based on these metrics

### Demo ###
![](https://github.com/cdy3870/llms_docker/blob/main/demo.gif)
