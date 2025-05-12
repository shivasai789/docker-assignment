FROM node:16-alpine 

ADD ./ /app 
WORKDIR /app 

RUN npm install 

ENTRYPOINT [ "node" ]
CMD [ "app.js" ]