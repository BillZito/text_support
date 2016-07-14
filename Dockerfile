FROM python:3.5

MAINTAINER mattjmcnaughton@gmail.com

# Add the code to `/sdep` and use as a dep.
ADD . /text_support
WORKDIR /text_support

# Update pip, download the development dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
