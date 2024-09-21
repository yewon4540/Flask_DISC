from flask import Flask, render_template, request, redirect, url_for, flash
import os
from analysis import analyze_responses
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    questions = load_questions()

    if request.method == 'POST':
        responses = []
        for i in range(1, len(questions["questions"]) + 1):
            answer = request.form.get(f'question_{i}')
            if not answer:
                flash(f'{i}번째 문항 미체크!', 'error')
                return render_template('survey.html', questions=questions["questions"])
            responses.append(answer)
        
        # Save the responses for analysis
        analyze_responses(responses)  # Call analysis code
        
        return redirect(url_for('result'))

    return render_template('survey.html', questions=questions["questions"])

@app.route('/result')
def result():
    # Load the analysis image and results
    analysis_image = os.path.join('static', 'images', 'analysis_graph.png')
    analysis_text, analysis_table = "Text Analysis Result", [["Type", "Score"], ["D", 5], ["I", 7], ["S", 4], ["C", 6]]
    
    return render_template('result.html', analysis_image=analysis_image, analysis_text=analysis_text, analysis_table=analysis_table)

if __name__ == '__main__':
    app.run(debug=True)
