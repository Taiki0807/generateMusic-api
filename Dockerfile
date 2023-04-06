FROM python:3.10.7-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
ADD requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "9000"]
