import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

font_path  = 'static/font/MalangmalangB.ttf'
fontprop = fm.FontProperties(fname=font_path)

def analyze_responses(responses, name, course):
    # 'D', 'I', 'S', 'C' 순서로 고정된 레이블과 대응하는 값 설정
    labels = ['C', 'S', 'I','D']
    values = [responses[3], responses[2], responses[1], responses[0]]
    
    # 막대 그래프의 색상 설정
    colors = ['blue', 'green', 'yellow', 'red']

    # 가로형 막대 그래프
    plt.barh(labels, values, color=colors)
    plt.xlabel('점수', fontproperties=fontprop)
    plt.ylabel('DISC 타입', fontproperties=fontprop)
    plt.title('DISC 분석 결과', fontproperties=fontprop)
    
    # 그래프 저장
    plt.savefig(f'static/images/{course}_{name}_analysis_graph.png')
    plt.close()

def analyze_overall_statistics():
    # 통계 정보를 불러옴 (PM8_all.csv 파일)
    try:
        # df = pd.read_csv('static/data/PM8_all.csv')
        df = pd.read_csv('static/data/JAVA8_all.csv')
        
    except FileNotFoundError:
        return None  # 파일이 없는 경우 처리

    # 각 DISC 유형별 합계 계산
    stats = {
        'D': df['D'].sum(),
        'I': df['I'].sum(),
        'S': df['S'].sum(),
        'C': df['C'].sum()
    }

    # 막대 그래프 생성
    labels = list(stats.keys())
    values = list(stats.values())
    colors = ['red', 'yellow', 'green', 'blue']

    # plt.bar(labels, values, color=colors)
    # plt.xlabel('DISC 유형', fontproperties=fontprop)
    # plt.ylabel('응답자 수', fontproperties=fontprop)
    # plt.title('DISC 유형별 통계', fontproperties=fontprop)
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
    
    plt.gca().set_aspect('equal')  # 그래프를 동그랗게 유지
    plt.title('DISC 유형별 통계', fontproperties=fontprop)

    # 그래프 저장
    plt.savefig('static/images/survey_statistics_graph.png')
    plt.close()

    return 'static/images/survey_statistics_graph.png'