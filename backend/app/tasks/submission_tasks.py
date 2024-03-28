import os
import uuid

from subprocess import Popen, PIPE

from .celery_app import celery_app, celery_logger


@celery_app.task
def process_submission(submitted_answer: str) -> str:
    temp_filename = write_user_code_to_file(submitted_answer)
    celery_logger.info(f"temp_filename is {temp_filename}")
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
    if temp_filename:
        os.remove(temp_filename)
        
    return f"Все ок я в норме. {result}"
    

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
