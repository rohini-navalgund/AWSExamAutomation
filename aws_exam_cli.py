import requests
import json

# =========================
# AWS API Endpoints
# =========================
CREATE_EXAM_URL      = "https://b7dmxrw1mg.execute-api.eu-west-1.amazonaws.com/default/createExam"
CREATE_QUESTION_URL  = "https://wk9kqqovee.execute-api.eu-west-1.amazonaws.com/default/createQuestion"
GET_QUESTIONS_URL    = "https://35rehpf4s0.execute-api.eu-west-1.amazonaws.com/default/getQuestions"
SUBMIT_EXAM_URL      = "https://p3kq30oena.execute-api.eu-west-1.amazonaws.com/default/submitExam"
GET_RESULTS_URL      = "https://k9cb6sn4qc.execute-api.eu-west-1.amazonaws.com/default/getResults"

# =========================
# Helper Functions
# =========================
def create_exam(exam_id, title, created_by):
    body = {
        "examId": exam_id,
        "title": title,
        "createdBy": created_by
    }
    resp = requests.post(CREATE_EXAM_URL, json=body)
    return resp.json()

def add_question(exam_id, question_text, options, correct_answer):
    body = {
        "examId": exam_id,
        "question": question_text,
        "options": options,
        "correctAnswer": correct_answer
    }
    resp = requests.post(CREATE_QUESTION_URL, json=body)
    return resp.json()

def fetch_questions(exam_id):
    url = f"{GET_QUESTIONS_URL}?examId={exam_id}"
    resp = requests.get(url)
    return resp.json()

def submit_exam(student_id, exam_id, answers):
    body = {
        "studentId": student_id,
        "examId": exam_id,
        "answers": answers
    }
    resp = requests.post(SUBMIT_EXAM_URL, json=body)
    return resp.json()

def get_results(student_id):
    url = f"{GET_RESULTS_URL}?studentId={student_id}"
    resp = requests.get(url)
    return resp.json()

# =========================
# CLI Flow
# =========================
def main():
    print("=== AWS Cloud Exam CLI ===\n")
    
    # Step 1: Create Exam
    exam_id = input("Enter Exam ID: ")
    title = input("Enter Exam Title: ")
    created_by = input("Created By: ")
    
    exam_resp = create_exam(exam_id, title, created_by)
    print("\nExam Created:", exam_resp.get("message"))
    
    # Step 2: Add Questions
    while True:
        add_q = input("\nDo you want to add a question? (y/n): ").lower()
        if add_q != 'y':
            break
        
        question_text = input("Question Text: ")
        options = [
            input("Option 1: "),
            input("Option 2: "),
            input("Option 3: "),
            input("Option 4: ")
        ]
        correct_answer = input("Correct Answer: ")
        
        q_resp = add_question(exam_id, question_text, options, correct_answer)
        q_id = q_resp['question']['questionId']
        print(f"Question Added with ID: {q_id}")
    
    # Step 3: Take Exam
    student_id = input("\nEnter Student ID to take exam: ")
    questions_resp = fetch_questions(exam_id)
    
    if "questions" not in questions_resp:
        print("Error fetching questions:", questions_resp)
        return
    
    answers = []
    for q in questions_resp['questions']:
        print("\nQuestion:", q['question'])
        for idx, opt in enumerate(q['options'], start=1):
            print(f"{idx}. {opt}")
        ans_idx = int(input("Select Option Number: "))
        answers.append({"questionId": q['questionId'], "answer": q['options'][ans_idx - 1]})
    
    # Step 4: Submit Exam
    submit_resp = submit_exam(student_id, exam_id, answers)
    print("\nExam Submitted!")
    print("Score:", submit_resp.get("score"))
    print("Correct Answers:", submit_resp.get("correctAnswers"))
    print("Total Questions:", submit_resp.get("totalQuestions"))
    
    # Step 5: Fetch Results
    results = get_results(student_id)
    print("\n=== Results ===")
    for r in results.get('results', []):
        print(f"Exam ID: {r['examId']}, Score: {r['score']}, Correct: {r['correctAnswers']}, Total: {r['totalQuestions']}")

if __name__ == "__main__":
    main()
