import matplotlib.pyplot as plt

def analyze_responses(responses):
    scores = {'D': 0, 'I': 0, 'S': 0, 'C': 0}
    for response in responses:
        scores[response] += 1

    labels = list(scores.keys())
    values = list(scores.values())

    plt.bar(labels, values)
    plt.xlabel('DISC Types')
    plt.ylabel('Score')
    plt.title('DISC Analysis Results')
    
    plt.savefig('static/images/analysis_graph.png')
    plt.close()
