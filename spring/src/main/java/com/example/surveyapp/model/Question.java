package com.example.surveyapp.model;

import java.util.List;

public class Question {
    private String text;           // 질문 내용
    private List<String> options;  // 선택지 목록

    public Question(String text, List<String> options) {
        this.text = text;
        this.options = options;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public List<String> getOptions() {
        return options;
    }

    public void setOptions(List<String> options) {
        this.options = options;
    }
}
