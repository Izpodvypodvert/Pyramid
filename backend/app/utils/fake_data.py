import requests


API_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{API_URL}/auth/register"
LOGIN_URL = f"{API_URL}/auth/jwt/login"
FAKE_USER = {"username": "user@example.com", "password": "string"}
FAKE_USER_WITH_EMAIL = {
    "email": "user@example.com",
    "password": "string",
    "username": "string",
}


def send_post_request(url, data, headers=None, use_json=True):
    if use_json:
        response = requests.post(url, json=data, headers=headers)
    else:
        response = requests.post(url, data=data, headers=headers)
    return response.status_code, response.json()


def register_user():
    status_code, response = send_post_request(REGISTER_URL, FAKE_USER_WITH_EMAIL)
    if status_code == 201:
        print(f"Successfully created record: {response}")
    else:
        print(f"Failed to create record: {response}")


def login_user():
    status_code, response = send_post_request(LOGIN_URL, FAKE_USER, use_json=False)
    if status_code == 200:
        print(f"Successfully logged in: {response}")
        return {"Authorization": f"Bearer {response['access_token']}"}
    else:
        raise Exception(f"Failed to log in: {response}")


def create_entity(endpoint, data, headers):
    url = f"{API_URL}/{endpoint}"
    status_code, response = send_post_request(url, data, headers=headers)
    if status_code == 200:
        print(f"Successfully created {endpoint[:-1]}: {response}")
        return response.get("id", response)
    else:
        print(f"Failed to create {endpoint[:-1]}: {response}")


def create_course(headers):
    course_data = {
        "title": "Big data",
        "programming_language": "python",
        "description": "Course about big data",
    }
    return create_entity("courses", course_data, headers)


def create_topic(course_id, headers):
    topic_data = {
        "order": 1,
        "course_id": course_id,
        "title": "Big data",
        "description": "about big data",
    }
    return create_entity("topics", topic_data, headers)


def create_lesson(topic_id, headers):
    lesson_data = {
        "order": 1,
        "topic_id": topic_id,
        "title": "Big data",
        "description": "about big data",
    }
    return create_entity("lessons", lesson_data, headers)


def create_step(lesson_id, course_id, step_kind, headers):
    step_data = {
        "order": 1,
        "lesson_id": lesson_id,
        "course_id": course_id,
        "step_kind": step_kind,
    }
    return create_entity("steps", step_data, headers)


def create_theory(step_id, headers):
    theory_data = {"step_id": step_id, "content": "theory here"}
    return create_entity("theories", theory_data, headers)


def create_test(step_id, headers):
    test_data = {"step_id": step_id, "question": "question?", "points": 0}
    return create_entity("tests", test_data, headers)


def create_test_choices(test_id, headers):
    test_choices_data = [
        {"test_id": test_id, "choice_text": "1", "is_correct": True},
        {"test_id": test_id, "choice_text": "2", "is_correct": False},
        {"test_id": test_id, "choice_text": "3", "is_correct": False},
    ]
    for choice_data in test_choices_data:
        create_entity("test-choices", choice_data, headers)


def create_coding_task(
    step_id, headers, instructions, solution_code, test_type, points=0
):
    coding_task_data = {
        "step_id": step_id,
        "instructions": instructions,
        "starter_code": "",
        "solution_code": solution_code,
        "simple_test_expected_output": (
            "" if test_type == "Advanced" else "Hello World!"
        ),
        "advanced_test_code": (
            ""
            if test_type == "Simple"
            else 'import unittest\n\n\nclass TestFibNums(unittest.TestCase):\n    def test_positive_numbers(self):\n        self.assertEqual(fib_nums(1), 1)\n        self.assertEqual(fib_nums(2), 1)\n        self.assertEqual(fib_nums(3), 2)\n        self.assertEqual(fib_nums(4), 3)\n        self.assertEqual(fib_nums(5), 5)\n        self.assertEqual(fib_nums(6), 8)\n\n    def test_zero_input(self):\n        with self.assertRaises(Exception):\n            fib_nums(0)\n\n    def test_negative_input(self):\n        with self.assertRaises(Exception):\n            fib_nums(-1)\n\n    def test_non_integer_input(self):\n        with self.assertRaises(TypeError):\n            fib_nums("string")\n            fib_nums(3.5)\n\n\nif __name__ == "__main__":\n    unittest.main()'
        ),
        "test_type": test_type,
        "points": points,
    }
    return create_entity("coding-tasks", coding_task_data, headers)


def submit_answer(step_id, answer, headers):
    submission_data = {"step_id": step_id, "submitted_answer": answer}
    return create_entity("submissions", submission_data, headers)


def main():
    register_user()
    headers = login_user()

    course_id = create_course(headers)
    topic_id = create_topic(course_id, headers)
    lesson_id = create_lesson(topic_id, headers)

    step_theory_id = create_step(lesson_id, course_id, "Theory", headers)
    theory_id = create_theory(step_theory_id, headers)

    step_test_id = create_step(lesson_id, course_id, "Test", headers)
    test_id = create_test(step_test_id, headers)
    create_test_choices(test_id, headers)
    submit_answer(step_test_id, "1", headers)

    step_coding_task_advanced_id = create_step(
        lesson_id, course_id, "CodingTask", headers
    )
    coding_task_advanced_id = create_coding_task(
        step_coding_task_advanced_id,
        headers,
        instructions="Write a function that generates fibonacci numbers.",
        solution_code='def fib_nums(number: int) -> int:\n    if number < 1:\n        raise Exception("Число должно быть больше нуля!")\n    if number in [1, 2]:\n        return 1\n    return fib_nums(number - 1) + fib_nums(number - 2)',
        test_type="Advanced",
    )
    submit_answer(
        step_coding_task_advanced_id,
        'def fib_nums(number: int) -> int:\n    if number < 1:\n        raise Exception("Число должно быть больше нуля!")\n    if number in [1, 2]:\n        return 1\n    return fib_nums(number - 1) + fib_nums(number - 2)',
        headers,
    )

    step_coding_task_simple_id = create_step(
        lesson_id, course_id, "CodingTask", headers
    )
    coding_task_simple_id = create_coding_task(
        step_coding_task_simple_id,
        headers,
        instructions="Output 'Hello World!' to the terminal.",
        solution_code="print('Hello World!')",
        test_type="Simple",
    )
    submit_answer(step_coding_task_simple_id, "print('Hello World!')", headers)


if __name__ == "__main__":
    main()
