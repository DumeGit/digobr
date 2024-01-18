import json

from flask import Flask, request
from openai import OpenAI
import re

app = Flask(__name__)
client = OpenAI()


@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    user_text = request.json.get('text')
    number = request.json.get('question_count')
    system_message = f'''
    You are an assistant exclusively dedicated to generating test questions in the Croatian language, presented in JSON format only. 
    Upon receiving a text prompt, it creates an array of exactly {number} questions, each as a JSON object. The questions are always in Croatian, irrespective of the input language. 
    Some questions should be easy(based on recognition), some medium(based on understanding of the subject), and some hard(based on conclusion) questions. 
    Each question object has a 'question' field with the question text in Croatian, and an 'answers' array with exactly four answers and one answer only is correct, but make it random which one in the list of answers is correct. 
    Each answer in this array features 'text' and 'correct' fields, with 'correct' as a boolean. The output is strictly in this format: 
    {{
    "quiz":[
    {{
     "question": string,
     "answers": [{{text: string, correct: boolean}}]
    }}
    ]
    }}
    Without any extraneous text or explanations before or after the JSON format, focusing solely on providing Croatian test questions in a structured JSON format.
    '''

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system",
             "content": system_message},
            {"role": "user", "content": user_text}
        ],
        response_format={"type": "json_object"},
    )

    response = completion.choices[0].message.content
    response = re.sub(r"[\n\t]*", "", response)
    response = response.replace('\\', '')
    quiz = json.loads(response)
    return quiz


if __name__ == '__main__':
    app.run(debug=True)
