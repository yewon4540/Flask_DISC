document.addEventListener('DOMContentLoaded', function () {
    const questions = {{ questions|tojson }};
    let currentQuestionIndex = 0;
    const totalQuestions = questions.length;

    function loadQuestion(index) {
        const questionElement = document.getElementById('question');
        const optionsElement = document.getElementById('options');
        const question = questions[index];
        questionElement.innerHTML = (index + 1) + ". " + question['question'];
        optionsElement.innerHTML = '';

        question['options'].forEach(option => {
            const optionHtml = `
                <label>
                    <input type="radio" name="question_${index}" value="${option.value}">
                    ${option.text}
                </label><br>
            `;
            optionsElement.insertAdjacentHTML('beforeend', optionHtml);
        });

        // '이전' 버튼 숨기기/보이기
        if (index === 0) {
            document.getElementById('prev').style.display = 'none';
        } else {
            document.getElementById('prev').style.display = 'inline-block';
        }

        // '다음' 버튼 텍스트 변경 (마지막 질문일 때 '제출')
        if (index === totalQuestions - 1) {
            document.getElementById('next').innerText = '제출';
        } else {
            document.getElementById('next').innerText = '다음';
        }
    }

    document.getElementById('next').addEventListener('click', function () {
        const options = document.querySelectorAll(`input[name="question_${currentQuestionIndex}"]`);
        let isChecked = false;
        options.forEach(option => {
            if (option.checked) {
                isChecked = true;
            }
        });

        if (!isChecked) {
            alert('항목에 체크해주세요.');
            return; // 체크되지 않은 경우 다음 질문으로 넘어가지 않음
        }

        if (currentQuestionIndex < totalQuestions - 1) {
            currentQuestionIndex++;
            loadQuestion(currentQuestionIndex);
        } else {
            window.location.href = "result.html"; // 제출 시 result.html로 이동
        }
    });

    document.getElementById('prev').addEventListener('click', function () {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            loadQuestion(currentQuestionIndex);
        }
    });

    // 첫 번째 질문 로드
    loadQuestion(currentQuestionIndex);