from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import pandas as pd
from analysis import analyze_responses, analyze_overall_statistics
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
        print("POST 요청 수신됨")

        
        name = request.form.get('name')
        session['name'] = name
        # course = 'PM8기'
        course = '풀스택 8기'
        # course = request.form.get('course') # 셀렉트 메소드 받아오기 아직 미구현
        session['course'] = course
        print(session['name'], session['course'])
        df = pd.DataFrame(columns=['D','I','S','C'])
        
        os.makedirs('static/data', exist_ok=True)
        df.to_csv(f'static/data/{course}_{name}.csv',index=False)
        print('save ok')

    return render_template('survey.html', questions=questions["questions"])

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    question_index = data.get('question_index')
    answer = data.get('answer')
    
    name = session.get('name')
    course = session.get('course')
    
    if not name or not course:
        return jsonify({"status": "error", "message": "사용자 정보가 없습니다."})
    
    
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
    
    name = session.get('name')
    course = session.get('course')
    
    if not name or not course:
        return jsonify({"status": "error", "message": "사용자 정보가 없습니다."})
    
    if request.method == 'POST':
        # print('hello')
        # answer_1 = request.form.get('question_1')
        # print(f"첫 번째 질문의 응답: {answer_1}")
                
        df = pd.read_csv(f'static/data/{course}_{name}.csv')
        responses = [df['D'].sum(),df['I'].sum(),df['S'].sum(),df['C'].sum()]
        analyze_responses(responses, name, course)
        print("응답 분석됨:", responses)
        
    analysis_image = os.path.join('static', 'images', f'{course}_{name}_analysis_graph.png')

    # CSV에서 응답 데이터를 로드
    df = pd.read_csv(f'static/data/{course}_{name}.csv')

    # DISC 유형별 점수 계산
    scores = {
        'D': df['D'].sum(),
        'I': df['I'].sum(),
        'S': df['S'].sum(),
        'C': df['C'].sum()
    }
    
    # 가장 높은 유형 계산
    max_score = max(scores.values())  # 가장 높은 점수
    max_types = [key for key, value in scores.items() if value == max_score]  # 가장 높은 점수를 가진 유형들

    # max_types 리스트는 가장 높은 점수의 유형들 ('D', 'I', 'S', 'C' 중)
    print(max_types)
    disc_type_str = ''.join(max_types)
    
    print('총합 불러오기')
    # df_all = pd.read_csv(f'static/data/PM8_all.csv')
    df_all = pd.read_csv(f'static/data/JAVA8_all.csv')
    print('총합 불러오기 성공!')
    df_all.loc[len(df_all)] = [course,name,0,0,0,0]
    
    for type_disc in disc_type_str:
        print(f"{type_disc}는~")
        try:
            df_all.loc[len(df_all)-1, type_disc] = 1/len(disc_type_str)
            print(f"{type_disc} = True")
        except:
            print('아몰랑')
            pass

    df_all.drop_duplicates(keep='last', inplace=True)
    df_all.reset_index(drop=True,inplace=True)
    df_all.to_csv(f'static/data/JAVA8_all.csv', index=False)
    stats_image = analyze_overall_statistics()
    
    stats_image = os.path.join('static', 'images', f'survey_statistics_graph.png')
    
    # return render_template('result.html', analysis_image=analysis_image, dataframe=df, scores=scores, disc_type_str=disc_type_str)
    return render_template('result.html', analysis_image=analysis_image, dataframe=df, scores=scores, disc_type_str=disc_type_str, stats_image=stats_image)

@app.route('/survey_statistics', methods=['GET'])
def survey_statistics():
    # 통계 정보를 읽어옴 (CSV 파일이나 DB)
    df = pd.read_csv('static/data/JAVA8_all.csv')
    # df = pd.read_csv('static/data/PM8_all.csv')  # 설문 결과가 저장된 CSV 파일
    stats = {
        'D': df['D'].sum(),
        'I': df['I'].sum(),
        'S': df['S'].sum(),
        'C': df['C'].sum()
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
