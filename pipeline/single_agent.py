import pandas as pd
import openai


openai.api_key = ''
def single_agent_zero_shot(statement):
    prompt = f"""
    Extend the following statement about kiin(restaurant in Toronto) into a more detailed review, try to add some restaurant information.
    
    Four criteria should be met to evaluate the generated reviews: 
    Consistency with user input, which evaluates whether the review reflects the user's original thoughts and includes key points the user wants to emphasize. 
    Contextual relevance, which evaluates whether the review contains relevant details about the restaurant, as accurate information enhances the credibility of the review. 
    Human-Like tone, which evaluates the review’s naturalness and fluency. A human-like tone makes the review more readable and trustworthy, which may increase its likelihood of being recognized as authentic by the platform.
    Overall Quality, which evaluates the review’s overall coherence, meaningfulness, and usefulness. 

    Let's think step by step

    User Input: "{statement}"
    Extended Review:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        top_p=1.0,
        max_tokens=200
    )

    return response['choices'][0]["message"]["content"].strip()


def single_agent_few_shot(statement):
    prompt = f"""
    You are a helpful assistant specializing in creating detailed restaurant reviews. 
    Based on the given user ideas about kiin(restaurant in Toronto), extend it into a more comprehensive review by adding restaurant information, 
    ambiance, menu highlights, and other relevant insights.

    Here are some examples:

    ### Example 1
    User Input: "The food was okay, but the service was slow."
    Extended Review: "The food at Kiin offers a decent variety of Thai-inspired flavors, 
    and while some dishes stand out, such as the Massaman curry, others could use a bit more vibrancy. 
    However, during my visit, the service pace was slower than expected, perhaps due to a busy evening. 
    That said, the staff remained courteous and tried their best to accommodate us, which I appreciated. The chic decor and authentic atmosphere still made for a pleasant dining experience."

    ### Example 2
    User Input: "The drinks are amazing, and the vibe is super trendy."
    Extended Review: "Kiin boasts an impressive drink menu, with creative cocktails like the 
    Tom Yum-tini that perfectly blend traditional Thai ingredients with a modern twist. 
    The trendy vibe, complete with elegant decor and soft lighting, makes it a go-to spot for both 
    casual evenings and special celebrations. Whether you're seated at the cozy bar or a stylish dining table, 
    the restaurant delivers a hip and vibrant atmosphere."

    Four criteria should be met to evaluate the generated reviews: 
    Consistency with user input, which evaluates whether the review reflects the user's original thoughts and includes key points the user wants to emphasize. 
    Contextual relevance, which evaluates whether the review contains relevant details about the restaurant, as accurate information enhances the credibility of the review. 
    Human-Like tone, which evaluates the review’s naturalness and fluency. A human-like tone makes the review more readable and trustworthy, which may increase its likelihood of being recognized as authentic by the platform.
    Overall Quality, which evaluates the review’s overall coherence, meaningfulness, and usefulness.

    Let's proceed step by step:
    - Step 1: Analyze the given statement.
    - Step 2: Add restaurant information to enrich the review.
    - Step 3: Write the review with a human-like tone.
    - Step 4: Ensure the review is coherent and useful.

    ### New Input
    User Input: "{statement}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        top_p=1.0,
        max_tokens=300
    )

    return response['choices'][0]["message"]["content"].strip()


input_statement = "This place is mind-blowing. The flavours are out of this world, the presentations are lovely, service is great."
input_statement2 = "This place is mind-blowing. Kho Yum is really excellent. Great service."
output_statement = single_agent_few_shot(input_statement)


print(f"Input: {input_statement2}")
print(f"Output: {output_statement}")
