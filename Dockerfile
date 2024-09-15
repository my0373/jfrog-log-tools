#
FROM python:latest
#
WORKDIR /code
#
COPY ./ /code

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
CMD ["python", "log_generator.py", "-h"]
