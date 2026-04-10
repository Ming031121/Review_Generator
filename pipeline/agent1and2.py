from openai import OpenAI
import requests
import requests
from bs4 import BeautifulSoup
import openai

# used to fetch and parse the restaurant webpage
def fetch_page_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.text  


agent1 = OpenAI()
agent2 = OpenAI()

inputs = ["This place is mind-blowing. Khao Yum is really excellent. Great service."]
restaurants = [("Kiin","https://www.tripadvisor.com/Restaurant_Review-g155019-d12501248-Reviews-Kiin-Toronto_Ontario.html")]
for i in range(len(inputs)):
    # fetch webpage contents
    agent2_input = fetch_page_content(restaurants[i][1])
    #print(agent2_input.split("\n\n")[:1])
    completion = agent2.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": "I will give you the contents of a restaurant's webpage in TripAdvisor. Please breifly summarize key points such as restaurant type, popular dishes and events in point form.\
                    Try to organize the information into a structured summary. For example: {cuisine style: ;popular dishes:; latest events:;}, include things that may help to draft a restaurant review.\n\
                        url:"+agent2_input
            }            
        ],
        max_tokens=300
    )
    agent2_out = completion.choices[0].message.content
    print(agent2_out)
    print("----------------------")
    # review generation
    completion1 = agent1.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": "I will give you a breif idea about the user's experience in the restaurant,"+restaurants[i][0]+", along with a summary of the restaurant-specific information.\
                    Please write a detailed restaurant review (no more than 150 words) based on the user's idea, the goal is to make the review be recognized as an authentic and high-quality one by online platforms like Yelp and Google Reviews. \
                    If anything in the restaurant summary can be related to the user's idea, try incorperating them to make the review more realisitic, but again, everything in the review should centered around the\
                    user's experience, do not mention anything in the restaurant summary that are irrelevant to user's idea. It's fine if you don't make use of restaurant summary. Just don't be far-fetched or make up things.\
                    Do not introduce the restaurant, try using 'I' instead of 'you', and avoid any introductory statements.  \
                    Please try to make the review coherant, meaningful, helpful. It's very importatnt to ensure it's in a human-like tone, so be careful about your word choice, avoid too complicated expression and make the review easily understood by people. \n\
                    Restaurant summary:"+agent2_out+"\nUser idea:"+ inputs[i]
            }            
        ],
        max_tokens=200
    )
    m_out = completion1.choices[0].message.content
    print(m_out)