FROM nginx:alpine

COPY app/ /app/
COPY app2/ /app2/
COPY other-steps/nginx.conf /etc/nginx/conf.d/default.conf
COPY other-steps/Another_One_Hint /app/Another_One_Hint

# COPY other-steps/admin.html /admin-html/admin.html
COPY other-steps/entrypoint.sh /entrypoint.sh

RUN apk update && apk add py3-pip bash tree
RUN pip install Flask==3.0.2 --break-system-packages
RUN chmod -R 777 /app /app2 /entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
 
