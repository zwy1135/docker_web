FROM fedora
RUN dnf install python3 python3-pip binutils -y
RUN dnf clean all
RUN mkdir -p ./application
RUN mkdir /transfer

WORKDIR /application

ADD ./requirements.txt /application

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ADD ./ /application

RUN pyinstaller -F -y ./main.py

WORKDIR /application/dist

EXPOSE 8080

CMD ["python3","-m","http.server","80"]

