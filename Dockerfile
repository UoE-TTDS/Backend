FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY . /app
RUN make /app
CMD python /app/app.py