from openai import OpenAI
import requests
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
agent3 = OpenAI()

df = pd.read_csv("../data/combine_res_info.csv")

inputs = df["Output"].tolist()
restaurants = list(zip(df["Restaurant"], df["Link"]))

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
                "content": 
                f"Write a restaurant review based on a brief user input about their experience at {restaurants[i][0]} and the restaurant summary, focusing on realism and human-like detail. Maximum length of the review is 150 words.\n\
                # Requirements: \n\
                - Expand on the user's idea naturally, and ensure the content remains realistic and authentic.\n\
                - Aim for an authentic and high-quality review that would be suitable for platforms like Yelp or Google Reviews.\n\
                - Elaborate on the user's input using relevant information from the restaurant summary, but avoid introducing too much new information beyond the user input.\n\
                - Instead of repeating qualities, describe how they are demonstrated through actions, behaviors, or experiences.\n\
                - Omit details from the restaurant summary that do not align with the user input.\n\
                - Do not make up information about the restaurant or user experience.\n\
                - Avoid introductory statements. Focus directly on the experience.\n\
                - Use 'I' instead of 'you' for a personal touch.\n\
                # Notes:   \n\
                - Consistency is key: Ensure the expanded details stay true to the user input.\n\
                - Avoid overly formal or mechanical expressions, and ensure the tone is human-like and conversational.\n\
                - Rewrite summary details into descriptions or vivid examples. Do not directly use the same words or phrases from the summary.\n\
                - Keep sentences short and simple, avoiding redundancy or overly verbose phrasing.\n\
                # Restaurant summary: {agent2_out}.\n\
                # User idea: {inputs[i]}"
            }
        ],
        max_tokens=200,
        temperature=1.3
    )
    m_out = completion1.choices[0].message.content
    print(f"Agent 1 Output:\n{m_out}")

    completion2 = agent3.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": f"You are tasked with refining and rewriting AI-generated restaurant reviews to make them sound more human-like and natural.\
                    Your goal is to eliminate overused or generic phrases and replace them with specific, and descriptive language, while keeping it oral and simple.\
                    Rewrite the provided review while maintaining the same meaning and tone. Ensure that the result is unique, conversational, and avoids repetitive expressions\n\
                    Requirements:\n\
                    - Replace generic phrases with action-oriented, contextually specific descriptions.\n\
                    - Keep sentences simple and short.\n\
                    - Avoid robotic or overly formal tone; write as if you were a real person sharing their personal experience.\n\
                    - Ensure coherence and maintain the core sentiment of the original review.\n\
                    Input Format: AI-Generated Review\n\
                    Output Format: Under title 'CoT', list the phrases that you think it's AI-like. Then under title 'Agent 3 Rewrite', give the human-refined review. Review should not exceed 150 words.\n\
                    Input:\n\{m_out}"
            }
        ],
         max_tokens=500,
        temperature=1.2
    )
    rewrite = completion2.choices[0].message.content
    print(f"\nAgent 3 Output:\n\n{rewrite}")
    print("----------------------")