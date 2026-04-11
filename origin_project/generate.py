import csv
import pandas as pd
import random
from openai import OpenAI
client = OpenAI(api_key="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")

combine_file = pd.read_csv("combine_output.csv", encoding="utf-8-sig")

sampled_reviews = combine_file["review"]

with open("prompt.txt", "r", encoding="utf-8-sig") as file:
    prompt_template = file.read()

results = []

def generate_summary(review, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[
                {"role": "system", "content": prompt_template},
                {"role": "user", "content": review}
        ],
        temperature=0.8,
        max_tokens=500,
        top_p=0.8
    )

    output = response.choices[0].message.content.strip('"')
    results.append((review, output))


for i, review in enumerate(sampled_reviews, start=1):
    generate_summary(review)


with open("output.csv", mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["Input", "Output"])
    for review, output in results:
        writer.writerow([review, output])

