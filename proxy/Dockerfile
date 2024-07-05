FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="rozdaruis@gmail.com"

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static

VOLUME /vol/static

USER nginx

CMD ["nginx", "-g", "daemon off;"]
