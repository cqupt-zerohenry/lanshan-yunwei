FROM python:3.9.7
COPY requirements.txt requirements.txt
COPY . /work/
WORKDIR /work
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python app4.py
