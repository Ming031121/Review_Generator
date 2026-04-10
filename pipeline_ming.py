from openai import OpenAI
import requests
import requests
from bs4 import BeautifulSoup
import openai
import os

def agent_1_review_generation(restaurants_name, user_idea, context, previous_generation=None, suggestions=None):
    if suggestions is None:
        message = [
            {
                "role": "assistant",
                "content":
                    f"Write a restaurant review based on a brief user input about their experience at {restaurants_name} and the restaurant summary, focusing on realism and human-like detail. Maximum length of the review is 150 words.\n\
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
                            # Restaurant summary: {context}.\n\
                            # User idea: {user_idea}"
            }
        ]
    else:
        message = [
            {
                "role": "assistant",
                "content":
                    f"you had already write a review about restaurant, same requriement as below, but now, someone give you how they comment it on the quality of review you write. they give you suggestion and score about your previous writing. \n"
                    f"Previous generated review: {previous_generation} \n"
                    f"Refinement suggestions: {suggestions} \n"       
                    f"now you need to rewrite a restaurant review based on a brief user input about their experience at {restaurants_name},the restaurant summary,and refinement suggestions, focusing on realism and human-like detail. Maximum length of the review is 150 words.\n\
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
                                    # Restaurant summary: {context}.\n\
                                    # User idea: {user_idea}"
            }
        ]

    completion1 = agent1.chat.completions.create(
        model="gpt-4o",
        messages=message,
        max_tokens=200,
        temperature=1.3
    )

    return completion1.choices[0].message.content

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

def agent_2_context_retrieval(restaurant_url):
    # Mocked data representing context retrieval from the webpage
    agent2_input = fetch_page_content(restaurant_url)
    print("input")
    print(agent2_input)
    print()
    # print(agent2_input.split("\n\n")[:1])
    completion2 = agent2.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": "I will give you the contents of a restaurant's webpage in TripAdvisor. Please breifly summarize key points such as restaurant type, popular dishes and events in point form.\
                        Try to organize the information into a structured summary. For example: {cuisine style: ;popular dishes:; latest events:;}, include things that may help to draft a restaurant review.\n\
                            url:" + agent2_input
            }
        ],
        max_tokens=300
    )
    # agent2_out = completion.choices[0].message.content
    # # print(agent2_out)
    return completion2.choices[0].message.content

# "1. Ensure that the review is engaging, informative, and easy to understand.\n"
# "2. Verify that the review appropriately reflects the provided context, such as the restaurant style, popular dishes, and event details.\n"
# "3. Check for grammatical errors, awkward phrasing, or any statements that may be misleading or inaccurate.\n"
def agent_3_quality_control(generated_review):
    completion3 = agent3.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": f"You are a quality control agent tasked with evaluating the quality of the following restaurant review:\n\n{generated_review}\n\n"
                    "Your task is to critically evaluate the review for clarity, completeness, tone, and accuracy. Specifically, you should:\n"
                    "1. do you think this review is real or not. Check the review writing is human like or ai like. the review should not look like ai writing. if the writing is ai-like, you should give a low rate on this comment\n"
                    "2. As a customer, how would you rate this review, do you think this review provide good and useful suggestion to you or not"
                    "If the review does not meet these criteria, provide a detailed list of improvement suggestions, specifying what needs to be modified and why.\n"
                    "Finally, rate the review base on above criteria, from scale 1 to 5, 1 is the worst, and 5 is the best \n"
                    "the output should follow the format below: \n"
                    "Rating: \n"
                    "Suggestions:"
            }
        ],
        max_tokens=500,
        temperature=1.2
    )
    output3 = completion3.choices[0].message.content

    rating = None
    for line in output3.splitlines():
        if line.lower().startswith("rating:"):
            try:
                rating = int(line.split(":")[1].strip())
            except ValueError:
                rating = None
    print(f"\nRATING OF agent3:{rating} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
    # Determine if the review passed the quality control
    if rating and rating >= 4:
        return True, "Review passed quality check."
    else:
        return False, output3

def run_pipeline(restaurants_name, restaurant_webpage, user_ideas):
    context = agent_2_context_retrieval(restaurant_webpage)

    generated_review = agent_1_review_generation(restaurants_name, user_ideas, context)
    print(f"first gen: {generated_review}\n\n")

    success, suggestions = agent_3_quality_control(generated_review)
    print(f"first suggestion: {suggestions}\n\n")

    count = 0
    max_retries = 3
    while not success and count < max_retries:

        generated_review = agent_1_review_generation(restaurants_name, user_ideas, context,
                                                     previous_generation=generated_review, suggestions=suggestions)
        success, suggestions  = agent_3_quality_control(generated_review)
        print(f"\n COUNT{count}!!!!!!!!!!!!!")
        print(generated_review)
        print()
        print(suggestions)
        print()
        count += 1

    return generated_review, count, success


if __name__ == "__main__":
    API_KEY = os.getenv("OPENAI_API_KEY")

    agent1 = OpenAI(api_key=API_KEY)
    agent2 = OpenAI(api_key=API_KEY)
    agent3 = OpenAI(api_key=API_KEY)
    restaurants_name = "Gyubee Japanese Grill (Dundas)"
    restaurant_url = "https://www.yelp.ca/biz/gyubee-japanese-grill-dundas-toronto"
    user_ideas = ("Outstanding dining at Gyubee. Cozy and lively vibe. Fresh and flavorful meats. Fantastic service. Highly recommend for Japanese BBQ lovers. Will definitely return!")

    review, count, success = run_pipeline(restaurant_url, restaurant_url, user_ideas)
    print(f"final_output:{review}\n"
          f"count: {count}\n"
          f"success: {success}")


