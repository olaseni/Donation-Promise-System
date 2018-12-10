FROM python:3.7.0-alpine
ENV PYTHONUNBUFFERED 1

ENV ENV="/etc/profile"
ENV PATH="${PATH}:/code/bin:/app/bin:/source/bin"

RUN apk update \
  && apk add --virtual build-deps gcc musl-dev \
  && apk add postgresql-dev postgresql-client openssh bash bash-completion \
  && apk add --no-cache jpeg-dev zlib-dev \
  && apk add --update make


RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN apk del build-deps
RUN /usr/bin/ssh-keygen -A ; /usr/sbin/sshd

RUN echo "export PATH=\$PATH:/code/bin:/app/bin:/source/bin" > /etc/profile.d/paths.sh
RUN echo "alias ll='ls -lh'" > /etc/profile.d/aliases.sh

LABEL description="An alpine python3 image with support for Django, postgres and sshd ..."
LABEL name="python:3.7.0-alpine/django-2.1"

RUN mkdir /src
WORKDIR /src
COPY src/ ./

EXPOSE 9000
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:9000"]