FROM python:3.12.2-slim@sha256:eb53cb99a609b86da6e239b16e1f2aed5e10cfbc538671fc4631093a00f133f2

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
    # --home "/nonexistent" \
    # --no-create-home \
    --uid "${UID}" \
    appuser && \
    chown appuser /project

COPY . docker_requirements.txt ./
RUN pip install -r docker_requirements.txt

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y ffmpeg 

RUN apt-get -y update \ 
    && apt-get install -y curl build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev

RUN pip install -U setuptools
RUN pip install dlib

RUN curl -LJO curl https://files.pythonhosted.org/packages/92/aa/fd00864e0bab93d084879bf149cb25d87850887199f0f1bebd16f926f3dc/face_recognition-0.1.11.tar.gz > face_recognition.tar.gz
RUN tar -xvzf face_recognition.tar.gz 
RUN cd face_recognition-0.1.11 && python3 setup.py install && cd ..

RUN pip install opencv-python-headless
RUN pip install ultralytics

USER appuser

COPY src ./src

CMD ["python" ,"src/tiktok-analyzer.py"]
