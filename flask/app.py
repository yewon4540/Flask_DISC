from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import pandas as pd
from analysis import analyze_responses
import json
# from flask_mysqldb import MySQL  # MariaDB 사용을 위한 라이브러리

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# # MariaDB 설정
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'alpaca'
# app.config['MYSQL_PASSWORD'] = 'niceday123!'
# app.config['MYSQL_DB'] = 'surveydb'
# mysql = MySQL(app)

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
        print("POST 요청 수신됨")

        globals()['name'] = request.form.get('name')
        globals()['course'] = request.form.get('course')
        print(name, course)
        globals()['df'] = pd.DataFrame(columns=['D','I','S','C'])
        
        os.makedirs('static/data', exist_ok=True)
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
        print('save ok')
        
        for i in range(1, len(questions["questions"]) + 1):
            answer = request.form.get(f'question_{i}')
            if answer:
                responses.append(answer)  # 응답 리스트에 추가
            else:
                flash(f'{i}번째 문항을 체크해주세요!', 'error')
                return render_template('survey.html', questions=questions["questions"])

        # 응답 데이터 처리 후 결과 페이지로 리디렉션
        analyze_responses(responses)  # 분석 로직 호출
        print("응답 분석됨:", responses)

        return redirect(url_for('result'))
        # return redirect(url_for('survey'))
    
        # for i in range(1, len(questions["questions"]) + 1):
        #     answer = request.form.get(f'question_{i}')
        #     if not answer:
        #         flash(f'{i}번째 문항 미체크!', 'error')
        #         return render_template('survey.html', questions=questions["questions"])
        #     responses.append(answer)
            
        #     if answer == 'D':
        #         df.loc[len(df)] = [1, 0, 0, 0]
        #         print('1')
        #     elif answer == 'I':
        #         df.loc[len(df)] = [0, 1, 0, 0]
        #         print('2')
        #     elif answer == 'S':
        #         df.loc[len(df)] = [0, 0, 1, 0]
        #         print('3')
        #     elif answer == 'C':
        #         df.loc[len(df)] = [0, 0, 0, 1]
        #         print('4')
        
        # df.to_csv(f'static/data/{course}_{name}.csv',index=False)

        # # 응답을 MariaDB에 저장
        # cur = mysql.connection.cursor()
        # for i, response in enumerate(responses):
        #     query = "INSERT INTO survey_responses (question, response) VALUES (%s, %s)"
        #     cur.execute(query, (questions["questions"][i]["question"], response))
        # mysql.connection.commit()
        # cur.close()

        # 응답 분석
        # analyze_responses(responses)
        # print("응답 분석됨:", responses)

        # # 결과 페이지로 리디렉션
        # return redirect(url_for('result'))

    return render_template('survey.html', questions=questions["questions"])
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    question_index = data.get('question_index')
    answer = data.get('answer')
    if answer == 'D':
        df = pd.read_csv(f'static/data/{course}_{name}.csv')
        df.loc[question_index-1] = [1, 0, 0, 0]
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
    elif answer == 'I':
        df = pd.read_csv(f'static/data/{course}_{name}.csv')
        df.loc[question_index-1] = [0, 1, 0, 0]
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
    elif answer == 'S':
        df = pd.read_csv(f'static/data/{course}_{name}.csv')
        df.loc[question_index-1] = [0, 0, 1, 0]
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
    elif answer == 'C':
        df = pd.read_csv(f'static/data/{course}_{name}.csv')
        df.loc[question_index-1] = [0, 0, 0, 1]
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
        
    # 여기서 받은 데이터를 처리 (예: 데이터베이스에 저장 등)
    print(f"질문 {question_index}에 대한 응답: {answer}")

    # 성공적인 응답 반환
    return jsonify({"status": "success", "message": f"질문 {question_index}에 대한 응답 저장 완료!"})

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        print('hello')
        answer_1 = request.form.get('question_1')
        print(f"첫 번째 질문의 응답: {answer_1}")
                
        analyze_responses(responses)
        print("응답 분석됨:", responses)
        
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
        
    analysis_image = os.path.join('static', 'images', 'analysis_graph.png')

    # CSV에서 응답 데이터를 로드
    df = pd.read_csv('static/data/survey_responses.csv')

    # DISC 유형별 점수 계산
    scores = df['Selected Value'].value_counts().to_dict()

    return render_template('result.html', analysis_image=analysis_image, scores=scores, dataframe=df)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
