from python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
copy . /usr/src/app

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD [ "bash", "run.sh" ]
