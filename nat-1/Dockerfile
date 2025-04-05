FROM nginx:alpine

COPY app/ /app/
COPY app/nginx.conf /etc/nginx/conf.d/default.conf
RUN apk update && apk add py3-pip bash
RUN pip install Flask==3.0.2 --break-system-packages
RUN chmod -R 777 /app

ENTRYPOINT [ "./app/entrypoint.sh" ]
 
