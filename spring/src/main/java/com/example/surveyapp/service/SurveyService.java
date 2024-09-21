package com.example.surveyapp.service;

import com.example.surveyapp.model.SurveyAnswers;
import com.example.surveyapp.model.Question;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SurveyService {

    public List<Question> getQuestions() {
        // 설문 문항 정의 (예시)
        return List.of(
            new Question("친구들과 그룹 과제를 할 때, 나는", List.of("D", "I", "S", "C")),
            new Question("새로운 사람들과 처음 만났을 때, 나는", List.of("D", "I", "S", "C"))
            // 나머지 질문 추가
        );
    }

    public boolean areAllQuestionsAnswered(SurveyAnswers surveyAnswers) {
        // 문항별 응답이 모두 체크되었는지 확인하는 로직
        return true; // 실제 로직 필요
    }

    public int getFirstUnansweredQuestion(SurveyAnswers surveyAnswers) {
        // 응답되지 않은 첫 문항 반환
        return 1; // 실제 로직 필요
    }

    public void analyze(SurveyAnswers surveyAnswers) {
        // Python 분석 코드를 실행하는 로직
    }

    public String getAnalysisText() {
        // 분석 결과 텍스트 반환
        return "분석 결과 텍스트";
    }

    public List<List<String>> getAnalysisTable() {
        // 분석 결과 표 반환 (예시)
        return List.of(
            List.of("분석 항목 1", "결과 1"),
            List.of("분석 항목 2", "결과 2")
        );
    }
}
