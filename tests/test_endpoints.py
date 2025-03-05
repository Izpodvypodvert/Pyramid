import pytest
from faker import Faker
import aiohttp
import pytest_asyncio

API_URL = "http://backend_test:8000/v1"
REGISTER_URL = f"{API_URL}/auth/register"
LOGIN_URL = f"{API_URL}/auth/jwt/login"

fake = Faker()


@pytest_asyncio.fixture
async def fake_user():
    return {"username": fake.email(), "password": "string"}


@pytest_asyncio.fixture
async def fake_user_with_email(fake_user):
    return {
        "email": fake_user["username"],
        "password": fake_user["password"],
        "username": "string",
    }


@pytest_asyncio.fixture
async def headers(fake_user, fake_user_with_email):
    status_code, response = await send_post_request(REGISTER_URL, fake_user_with_email)
    assert status_code == 201, f"Failed to register user: {response}"

    status_code, response = await send_post_request(
        LOGIN_URL, fake_user, use_json=False
    )
    assert status_code == 200, f"Failed to log in: {response}"

    return {"Authorization": f"Bearer {response['access_token']}"}


async def send_post_request(url, data, headers=None, use_json=True):
    async with aiohttp.ClientSession() as session:
        if use_json:
            async with session.post(url, json=data, headers=headers) as response:
                response_data = await response.json()
                return response.status, response_data
        else:
            async with session.post(url, data=data, headers=headers) as response:
                response_data = await response.json()
                return response.status, response_data


async def create_entity(endpoint, data, headers):
    url = f"{API_URL}/{endpoint}"
    status_code, response = await send_post_request(url, data, headers=headers)
    assert status_code == 200, f"Failed to create {endpoint[:-1]}: {response}"
    return response.get("id", response)


@pytest.mark.asyncio
async def test_create_course(headers):
    course_data = {
        "title": "Big data",
        "programming_language": "python",
        "description": "Course about big data",
    }
    course_id = await create_entity("courses", course_data, headers)
    assert course_id is not None, "Failed to create course"
    return course_id


@pytest.mark.asyncio
async def test_create_topic(headers):
    course_id = await test_create_course(headers)
    topic_data = {
        "order": 1,
        "course_id": course_id,
        "title": "Big data",
        "description": "about big data",
    }
    topic_id = await create_entity("topics", topic_data, headers)
    assert topic_id is not None, "Failed to create topic"
    return topic_id


@pytest.mark.asyncio
async def test_create_lesson(headers):
    course_id = await test_create_course(headers)
    topic_id = await test_create_topic(headers)
    lesson_data = {
        "order": 1,
        "topic_id": topic_id,
        "title": "Big data",
        "description": "about big data",
    }
    lesson_id = await create_entity("lessons", lesson_data, headers)
    assert lesson_id is not None, "Failed to create lesson"
    return lesson_id


@pytest.mark.asyncio
async def test_create_theory(headers):
    course_id = await test_create_course(headers)
    topic_id = await test_create_topic(headers)
    lesson_id = await test_create_lesson(headers)

    step_theory_id = await create_entity(
        "steps",
        {
            "order": 1,
            "lesson_id": lesson_id,
            "course_id": course_id,
            "step_kind": "Theory",
        },
        headers,
    )
    assert step_theory_id is not None, "Failed to create step theory"

    theory_data = {"step_id": step_theory_id, "content": "theory here"}
    theory_id = await create_entity("theories", theory_data, headers)
    assert theory_id is not None, "Failed to create theory"


@pytest.mark.asyncio
async def test_create_test(headers):
    course_id = await test_create_course(headers)
    topic_id = await test_create_topic(headers)
    lesson_id = await test_create_lesson(headers)

    step_test_id = await create_entity(
        "steps",
        {
            "order": 1,
            "lesson_id": lesson_id,
            "course_id": course_id,
            "step_kind": "Test",
        },
        headers,
    )
    assert step_test_id is not None, "Failed to create step test"

    test_data = {"step_id": step_test_id, "question": "question?", "points": 0}
    test_id = await create_entity("tests", test_data, headers)
    assert test_id is not None, "Failed to create test"


@pytest.mark.asyncio
async def test_create_coding_task(headers):
    course_id = await test_create_course(headers)
    topic_id = await test_create_topic(headers)
    lesson_id = await test_create_lesson(headers)

    step_coding_task_id = await create_entity(
        "steps",
        {
            "order": 1,
            "lesson_id": lesson_id,
            "course_id": course_id,
            "step_kind": "CodingTask",
        },
        headers,
    )
    assert step_coding_task_id is not None, "Failed to create step coding task"

    coding_task_data = {
        "step_id": step_coding_task_id,
        "instructions": "Write a function that generates fibonacci numbers.",
        "solution_code": 'def fib_nums(number: int) -> int:\n    if number < 1:\n        raise Exception("Число должно быть больше нуля!")\n    if number in [1, 2]:\n        return 1\n    return fib_nums(number - 1) + fib_nums(number - 2)',
        "simple_test_expected_output": "",
        "advanced_test_code": 'import unittest\n\n\nclass TestFibNums(unittest.TestCase):\n    def test_positive_numbers(self):\n        self.assertEqual(fib_nums(1), 1)\n        self.assertEqual(fib_nums(2), 1)\n        self.assertEqual(fib_nums(3), 2)\n        self.assertEqual(fib_nums(4), 3)\n        self.assertEqual(fib_nums(5), 5)\n        self.assertEqual(fib_nums(6), 8)\n\n    def test_zero_input(self):\n        with self.assertRaises(Exception):\n            fib_nums(0)\n\n    def test_negative_input(self):\n        with self.assertRaises(Exception):\n            fib_nums(-1)\n\n    def test_non_integer_input(self):\n        with self.assertRaises(TypeError):\n            fib_nums("string")\n            fib_nums(3.5)\n\n\nif __name__ == "__main__":\n    unittest.main()',
        "test_type": "Advanced",
        "points": 0,
    }
    coding_task_id = await create_entity("coding-tasks", coding_task_data, headers)
    assert coding_task_id is not None, "Failed to create coding task"
