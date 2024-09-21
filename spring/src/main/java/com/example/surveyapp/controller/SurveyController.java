package com.example.surveyapp.controller;

import com.example.surveyapp.model.UserInput;
import com.example.surveyapp.model.SurveyAnswers;
import com.example.surveyapp.service.SurveyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class SurveyController {

    @Autowired
    private SurveyService surveyService;

    @GetMapping("/")
    public String getInitialPage(Model model) {
        model.addAttribute("userInput", new UserInput());
        return "initialPage";
    }

    @PostMapping("/start-survey")
    public String startSurvey(@ModelAttribute UserInput userInput, Model model) {
        model.addAttribute("questions", surveyService.getQuestions());
        model.addAttribute("userInput", userInput);
        return "surveyPage";
    }

    @PostMapping("/submit-survey")
    public String submitSurvey(@ModelAttribute SurveyAnswers surveyAnswers, Model model) {
        if (!surveyService.areAllQuestionsAnswered(surveyAnswers)) {
            int missingQuestion = surveyService.getFirstUnansweredQuestion(surveyAnswers);
            model.addAttribute("alertMessage", missingQuestion + "번째 문항 미체크!");
            return "surveyPage";
        }

        surveyService.analyze(surveyAnswers);
        return "redirect:/results";
    }

    @GetMapping("/results")
    public String getResultsPage(Model model) {
        model.addAttribute("graphPath", "/images/graph.png");
        model.addAttribute("analysisText", surveyService.getAnalysisText());
        model.addAttribute("analysisTable", surveyService.getAnalysisTable());
        return "resultsPage";
    }
}
