FROM alpine:3.7

WORKDIR /app

COPY . /app


RUN apk add --no-cache python-dev
RUN apk add --no-cache py-pip
RUN pip install flask
RUN pip install flask_cors
RUN pip install requests

EXPOSE 80

ENV TEAM_ID=CC_072_073_075_091

CMD ["python", "acts.py"]
