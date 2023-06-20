#Base image which we want to build our custom image from
FROM python:3.9.7

#from where commands has to be run
WORKDIR /usr/src/app

#we are copying the file which is on our host to our conatiner in /usr/arc/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#Copy whatever is in our current directory i.e alembic, app into /use/src/app
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]