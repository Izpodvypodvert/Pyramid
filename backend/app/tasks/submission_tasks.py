import os
import uuid

from subprocess import Popen, PIPE

from .celery_app import celery_app, celery_logger


@celery_app.task
def process_submission(submitted_answer: str) -> str:
    """
    Processes a simple submission without additional test code.
    """
    temp_filename = write_user_code_to_file(submitted_answer)

    try:
        return run_code_in_docker(temp_filename)
    finally:
        if temp_filename:
            os.remove(temp_filename)


@celery_app.task
def process_submission_with_advanced_test_code(
    submitted_answer: str, advanced_test_code: str
) -> str:
    """
    Processes a submission with additional advanced test code.
    """
    temp_filename = write_user_code_with_tests_to_file(
        submitted_answer, advanced_test_code
    )

    try:
        return run_code_in_docker(temp_filename)
    finally:
        if temp_filename:
            os.remove(temp_filename)


def run_code_in_docker(temp_filename: str) -> str:
    """
    Runs the specified code file in a Docker container and returns the output.
    """
    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        "pyramid_shared_vol:/app",
        "python:3.12.1-alpine",
        "python",
        f"/app/{os.path.basename(temp_filename)}",
    ]
    result = create_subprocess(command)
    return result.strip()


def create_subprocess(program: list[str]):
    process = Popen(program, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    if stdout is not None:
        return stdout.decode()
    elif stderr is not None:
        return stderr.decode()
    else:
        return "Процесс не вернул вывода."


def write_user_code_to_file(user_code: str) -> str:
    temp_filename = f"/app/code_{uuid.uuid4().hex}.py"

    with open(temp_filename, "w") as f:
        f.write(user_code)
    return temp_filename


def write_user_code_with_tests_to_file(user_code: str, test_code: str) -> str:
    temp_filename = f"/app/code_{uuid.uuid4().hex}.py"

    with open(temp_filename, "w") as f:
        f.write(user_code + "\n\n")
        f.write(test_code)
    return temp_filename
