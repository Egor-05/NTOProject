FROM python:3
ENV PYTHONUNBUFFERED 1
COPY ./ /Users/USER/PycharmProjects/NTOProject/NTO
WORKDIR /app
EXPOSE 8000
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
CMD ["python3", "manage.py", "runserver"]