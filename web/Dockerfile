FROM frolvlad/alpine-glibc
  
RUN mkdir -p /web

RUN apk add --update wget

WORKDIR /web

ADD ./entrypoint.sh /web

RUN chmod u+x ./entrypoint.sh

ADD ./static /web/static

ADD ./templates /web/templates

EXPOSE 8000

CMD ["/bin/sh","./entrypoint.sh"]