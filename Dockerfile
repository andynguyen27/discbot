FROM python
WORKDIR /discbot
COPY . /discbot
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["python3","main.py"]