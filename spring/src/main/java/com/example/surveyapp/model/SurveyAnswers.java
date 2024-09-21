package com.example.surveyapp.model;

import java.util.Map;

public class SurveyAnswers {
    private Map<Integer, String> answers;  // 각 질문의 번호와 응답

    public Map<Integer, String> getAnswers() {
        return answers;
    }

    public void setAnswers(Map<Integer, String> answers) {
        this.answers = answers;
    }
}
