
"""
AWS Cloud Exam Automation - Fully Automated
Author: Your Name
Date: 2026-02-07
Description:
- Create exams
- Add multiple questions
- Simulate multiple students taking exams
- Submit answers (random or correct)
- Fetch and save results to CSV
- Fully automated without frontend
"""

import requests
import json
import csv
import random
from datetime import datetime

# ============================
# ----- Step 0: API URLs -----
# ============================
CREATE_EXAM_URL      = "https://b7dmxrw1mg.execute-api.eu-west-1.amazonaws.com/default/createExam"
CREATE_QUESTION_URL  = "https://wk9kqqovee.execute-api.eu-west-1.amazonaws.com/default/createQuestion"
GET_QUESTIONS_URL    = "https://35rehpf4s0.execute-api.eu-west-1.amazonaws.com/default/getQuestions"
SUBMIT_EXAM_URL      = "https://p3kq30oena.execute-api.eu-west-1.amazonaws.com/default/submitExam"
GET_RESULTS_URL      = "https://k9cb6sn4qc.execute-api.eu-west-1.amazonaws.com/default/getResults"

# ============================
# ----- Configurations -----
# ============================
EXAM_ID      = "exam010"
EXAM_TITLE   = "AWS Full Automation Exam"
CREATED_BY   = "admin"

QUESTIONS = [
    {
        "question": "Which AWS service is fully serverless?",
        "options": ["EC2", "Lambda", "ECS", "Lightsail"],
        "correct": "Lambda"
    },
    {
        "question": "Which AWS service is used for object storage?",
        "options": ["S3", "EBS", "EFS", "FSx"],
        "correct": "S3"
    },
    {
        "question": "Which AWS service is a managed relational database?",
        "options": ["DynamoDB", "Aurora", "Redshift", "RDS"],
        "correct": "RDS"
    },
    {
        "question": "Which AWS service provides DNS routing?",
        "options": ["Route 53", "CloudFront", "API Gateway", "VPC"],
        "correct": "Route 53"
    },
    {
        "question": "Which AWS service provides a content delivery network?",
        "options": ["CloudFront", "S3", "ECS", "Lambda"],
        "correct": "CloudFront"
    },
]

STUDENTS = ["student1001", "student1002", "student1003"]

USE_RANDOM_ANSWERS = True  # True = random answers, False = always correct answers

RESULT_CSV_FILE = f"AWSExamResults_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# ============================
# ----- Helper Functions -----
# ============================
def create_exam(exam_id, title, created_by):
    body = {
        "examId": exam_id,
        "title": title,
        "createdBy": created_by
    }
    response = requests.post(CREATE_EXAM_URL, json=body).json()
    print(f"Exam Created: {response.get('message')}")
    return response

def add_question(exam_id, question_text, options, correct_answer):
    body = {
        "examId": exam_id,
        "question": question_text,
        "options": options,
        "correctAnswer": correct_answer
    }
    response = requests.post(CREATE_QUESTION_URL, json=body).json()
    question_id = response['question']['questionId']
    print(f"Question Added: {question_text} (ID: {question_id})")
    return question_id

def fetch_questions(exam_id):
    url = f"{GET_QUESTIONS_URL}?examId={exam_id}".strip()
    response = requests.get(url).json()
    questions = response.get('questions', [])
    print(f"\nFetched {len(questions)} Questions for Exam {exam_id}.")
    return questions

def submit_exam(student_id, exam_id, questions, use_random=True):
    answers = []
    for q in questions:
        if use_random:
            answer = random.choice(q['options'])
        else:
            answer = q['correctAnswer']
        answers.append({"questionId": q['questionId'], "answer": answer})
        print(f"Answering Question ID {q['questionId']} with: {answer}")
    body = {"studentId": student_id, "examId": exam_id, "answers": answers}
    response = requests.post(SUBMIT_EXAM_URL, json=body).json()
    print(f"\nExam Submitted for Student {student_id}")
    print(f"Score: {response.get('score')}, Correct Answers: {response.get('correctAnswers')}, Total Questions: {response.get('totalQuestions')}")
    return response

def fetch_results(student_id):
    url = f"{GET_RESULTS_URL}?studentId={student_id}".strip()
    response = requests.get(url).json()
    results = response.get('results', [])
    print(f"\nResults for Student {student_id}:")
    for r in results:
        print(f"- Exam {r['examId']}: Score {r['score']}, Correct {r['correctAnswers']}, Total {r['totalQuestions']}")
    return results

def save_results_to_csv(all_results, filename):
    keys = ["studentId", "examId", "score", "correctAnswers", "totalQuestions", "submittedAt"]
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for result in all_results:
            for r in result:
                writer.writerow(r)
    print(f"\nAll results saved to {filename}")

# ============================
# ----- Main Execution -----
# ============================
if __name__ == "__main__":
    # Step 1: Create Exam
    create_exam(EXAM_ID, EXAM_TITLE, CREATED_BY)

    # Step 2: Add Questions
    question_ids = []
    for q in QUESTIONS:
        q_id = add_question(EXAM_ID, q['question'], q['options'], q['correct'])
        q['questionId'] = q_id
        question_ids.append(q_id)

    # Step 3 & 4: Students take Exam
    all_results = []
    for student in STUDENTS:
        questions = fetch_questions(EXAM_ID)
        result = submit_exam(student, EXAM_ID, questions, use_random=USE_RANDOM_ANSWERS)
        all_results.append([{
            "studentId": student,
            "examId": result['examId'],
            "score": result['score'],
            "correctAnswers": result['correctAnswers'],
            "totalQuestions": result['totalQuestions'],
            "submittedAt": result.get('submittedAt', datetime.now().isoformat())
        }])

    # Step 5: Fetch Results and Save CSV
    for student in STUDENTS:
        fetch_results(student)
    save_results_to_csv(all_results, RESULT_CSV_FILE)
