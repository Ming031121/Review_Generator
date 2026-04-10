import csv
import openai
import random
openai.api_key = "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"

def read_csv(file_path):
    input_list = []
    with open(file_path, mode='r',encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            input_list.append(row)
    return input_list
def write_csv(output_file_path, data):
    with open(output_file_path,mode='w',encoding="utf-8",newline='') as file:
        writer = csv.writer(file)
        # title?
        for row in data:
            writer.writerow([row])

def reverse_review_to_hint(review):
    messages1 = [
        {"role":"system", "content": '''You are an AI Data Engineer working on a project.the project is going to receive Now you have some data which is the high quality restaurant review 
        that you collect and your goal is to .For the following customer review, analyze 
        and extract the key information into the following attributes:
        
        You are working on a project called "Reviewal," which aims to generate high-quality restaurant reviews 
        based on user-provided information or hints. The idea is to leverage existing data to create a model 
        that can provide useful and authentic reviews for Google Maps or similar platforms.
        
        Currently, you're in the data collection phase. You've gathered high-quality reviews and are now focusing 
        on reverse-engineering them that given the collected output review, what kinds of input will let the model 
        generate those output.'''
         },
        {"role": "user", "content":(
            "your task is to predict what kinds of user input will let the auto review generative model generated such "
            "output review you will only need to return the user input you predict"
            f"generated review:{review}\n\n"
        )}
    ]

    messages2 = [
        {"role": "system", "content": '''You are an very smart AI Data Engineer who working on a project.'''},
        {"role": "user", "content": (
            "suppose there is a model called reviewpal, the model will generate a high quality review from the user "
            "hint and now you will receive some generated review by that model, and you need to predict what user input "
            "to the model that have such generate output"
            "you will only need to return the user input you predict"
            "Example:"
            "Generated review: I had been to Piano Piano before, but this time I took my girlfriend for lunch, and it was even better "
            "than I remembered!  The atmosphere was perfect for a relaxed midday meal, and the service was "
            "fantastic—attentive yet unobtrusive.  The lunch special was impressive, and every dish we ordered "
            "was full of flavor and beautifully presented.  My girlfriend loved it as much as I did, and it made "
            "for a perfect date.  From the delicious food to the cozy ambiance, Piano Piano continues to impress."
            "your predict output:"
            "Went to Piano Piano for lunch with my girlfriend. The food had really good flavor and was beautifully"
            "presented. We both really enjoyed it, especially the cozy atmosphere. Service was great—attentive but not too "
            "much. Definitely plan to go back."
            "We’ll definitely be back!"
            f"generated review:{review}\n\n"
            "Your prediction:"
        )}
    ]

    messages = [
        {"role": "user", "content":
            '''
            Given a restaurant review, summarize it to simulate user input as a quick thought.
            ## The summarized user quick thought should satisfy the following points:
            - Be concise, like a quick thought someone might share.
            - Accurately reflect the original user's main idea or sentiment.
            - Do not introduce new ideas or alter the user's original intent.
            - If provided, the following key features should be kept but simplified: dishes (with more descriptive details), tastes, vibe, environment, services, sentiment, suggestion.
            - Keep numeric data.
            - Can be in the format of short phrases or simple sentences, such as:
              - "Good vibe."
              - "Will come back."
              - "Friendly staff."
            
            ## Process:
            - Extract the key points.
            - Treat each key point as a sentence. Append the sentences.
            
            ## Example:
            
            ### Input review:
            "I absolutely love this place!!!! 5/5 nothing bad to say.
            
            My friend and I came to PAI on a Friday night with no reservation after seeing all their reservations were booked up. We still went to take our chances with walk in around 7pm and we got a table within 15 mins! It was super busy yet they were still able to seat many of us who walked in.
            
            The place upon entrance looks small but it is MASSIVE inside. The vibes are so good with the decor and the lighting. We both only wanted a main as we needed to leave pretty quickly. Service was super fast and friendly.
            
            Food:
            - Pad Thai with Beef (no chives): 5/5 stars. I was absolutely starving and this was phenomenal. It was not too sweet or sour. It was perfect. Texture was great and portions were pretty big. I could've taken some home if I wanted to but was too hungry.
            
            As we were in a rush, we were able to leave within 45 mins of being there. 5/5!!! Would recommend even if you don't have a reso"
            
            ### Output quick thought:
            "Love this place. Great vibe. Fast service. Amazing Pad Thai with balanced taste and great texture. Walked in on a busy night and seated fast in 15 min. Can finish in 45 min. Recommended. Would rate 5/5."
            
            ## Notes
            - Keep it simple.
            - Prefer short phrases that are more descriptive of the dishes mentioned.
            '''
            f"input review:{review}\n\n"
            "Your Output quick thought:"
            }
    ]



    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages2,
        max_tokens=100,
        temperature=0.8,
        top_p=0.8
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    input_file = "output.csv"
    file_list = read_csv(input_file)
    input_list = [row[0] for row in file_list]
    output_list = [row[1] for row in file_list]

    avg_len_input = sum([len(sentence) for sentence in input_list])/len(input_list)
    print(avg_len_input)
    avg_len_output = sum([len(sentence) for sentence in output_list]) / len(output_list)
    print(avg_len_output)



    # for row in random_list:
    #     print("input")
    #     print(row)
    #     print("output")
    #     extract_input = reverse_review_to_hint(row)
    #     print(extract_input)
    #     extract_list.append(extract_input)
    # write_csv("extract_user_input.csv", extract_list)
    #



#
#     first_example = '''I've never had Thai breakfast before, and being somewhat of a brunch enthusiast, I immediately made a reservation when I found out that Kiin now does brunch!
#
# When I first stepped into Kiin I fell in love with the light airy aesthetic of the place, everything was so beautiful. We started with the Rama Caesar, which tastes like a regular Caesar but with Tom Yum soup as a base. The Thai iced coffee was also pretty good but I found it quite similar to Vietnamese iced coffee.
#
# We got all three of the brunch items and they were spectacularly presented and tasted equally as good. I especially enjoyed the Thai crullers that came with the Khai Kratha. We ended the meal with some donuts and they were also very good.
#
# While I wouldn't say the brunch was the best food I've ever had, dining at Kiin was definitely an exciting culinary experience. Thai breakfast was something I've never tried before, the aesthetic of the restaurant was pleasing and the service attentive. Overall a great experience.
#
#     '''
#     print(first_example)
#     extract_input = reverse_review_to_hint(first_example)
#     print("\noutput\n")
#     print(extract_input)
#
#


