FROM python:3.8
WORKDIR /project
ADD . /project
RUN pip install -r docker_requirements.txt
CMD ["python","deploy.py"]