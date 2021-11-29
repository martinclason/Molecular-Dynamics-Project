# Get the python 3.9 base docker image
FROM python:3.9
RUN apt-get update && apt-get install software-properties-common
RUN add-apt-repository ppa:openkim/latest
RUN apt-get install libkim-api-dev openkim-models
RUN python -m pip install --upgrade pip
RUN pip install flake8 pytest wheel numpy scipy ase pyyaml kimpy
RUN pip install asap3
RUN flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
RUN flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
RUN python3 -m pytest
# Copy your Pipfile and Pipfile.lock in your container
#RUN pip install pipenv
#COPY Pipfile .
#COPY Pipfile.lock .
# Install all the dependencies from your lock file directly into the # container
#RUN pipenv install — system — deploy