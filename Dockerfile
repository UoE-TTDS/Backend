FROM tiangolo/uwsgi-nginx-flask:python3.7
ADD run.py /
CMD [ "python", "./app/app.py" ]