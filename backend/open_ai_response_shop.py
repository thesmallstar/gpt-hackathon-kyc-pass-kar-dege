import os
import openai
import json
from flask import jsonify

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response_from_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response


def generate_ocr_result_for_unknown(text, questions):
    # print(text)
    my_string = "Create a json for knowing" + ", ".join(questions) + " and return in a simple and not nested json, each value should be string only?"
    question1 = text.strip()[:4000] + my_string
    ai_response1 = get_response_from_openai(question1)
    print(ai_response1)


    result = ai_response1['choices'][0]['message']['content']

    result = json.loads(result)
    return jsonify(result)


def generate_ocr_result_for_shop(text):
    # print(text)
    my_string = "Create a json for knowing name of establishment , name of person owning the shop, is this a valid shop establishment document in india? why? and return in a json with appropriate keys and send every value as string?"
    question1 = text.strip()[:4000] + my_string
    ai_response1 = get_response_from_openai(question1)
    print(ai_response1)

    result = ai_response1['choices'][0]['message']['content']

    result = json.loads(result)
    return jsonify(result)

def generate_ocr_result_for_partnership(text):
    # print(text)
    my_string = "Create a json for knowing name of firm , name of partners, is this a valid partnership deed document in india? why? and return in a json with appropriate keys and send every value as string only. send name_of_partners as comma separated string?"
    question1 = text.strip()[:4000] + my_string
    ai_response1 = get_response_from_openai(question1)
    print(ai_response1)

    result = ai_response1['choices'][0]['message']['content']

    result = json.loads(result)
    return jsonify(result)