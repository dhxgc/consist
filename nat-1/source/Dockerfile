FROM nginx:alpine

COPY app/ /app/
COPY app2/ /app2/
COPY other-steps/.htpasswd /etc/nginx/.htpasswd
COPY other-steps/nginx.conf /etc/nginx/conf.d/default.conf
COPY other-steps/entrypoint.sh /entrypoint.sh
COPY other-steps/messages.db /app/messages.db

RUN apk update && apk add py3-pip bash tree
RUN pip install Flask==3.0.2 --break-system-packages
RUN echo "flag{Congratulations, you're root...}" > /root/flag.txt
RUN chmod -R 777 /app /app2 /entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
 
