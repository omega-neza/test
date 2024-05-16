from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.5)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

knowledge_base = load_knowledge_base('knowledge_base.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.form['user_question']

    if user_question.lower() == 'quit':
        return "Goodbye!"

    best_match = find_best_match(user_question, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return answer
    else:
        return "I don't know the answer. Can you teach me?"

@app.route('/teach', methods=['POST'])
def teach_bot():
    user_question = request.form['user_question']
    new_answer = request.form['new_answer']

    # Update knowledge base
    knowledge_base["questions"].append({"question": user_question, "answer": new_answer})
    save_knowledge_base('knowledge_base.json', knowledge_base)

    return "Thanks for teaching me"

if __name__ == '__main__':
    app.run(debug=True)
