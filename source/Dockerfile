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


RUN cp -f ./dist/main /transfer/

CMD ["cp","-f","./dist/main","/transfer/"]

