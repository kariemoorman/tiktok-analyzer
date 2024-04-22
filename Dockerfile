FROM python:3.12.2-slim@sha256:eb53cb99a609b86da6e239b16e1f2aed5e10cfbc538671fc4631093a00f133f2


#ENV TINI_VERSION v0.19.0
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
#RUN chmod +x /tini
#ENTRYPOINT ["/tini", "--"]

RUN pip install -U \
    pip \
    setuptools \
    wheel

WORKDIR /project

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
 #   --home "/nonexistent" \
 #   --no-create-home \
    --uid "${UID}" \
    appuser && \
    chown appuser /project

COPY . requirements.txt ./
RUN pip install -r docker_requirements.txt

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN pip install opencv-python-headless

COPY . .

USER appuser

CMD ["python" ,"src/tiktok-analyzer.py"]
