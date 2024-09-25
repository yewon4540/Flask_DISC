import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

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
