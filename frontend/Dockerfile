FROM node:13-slim

WORKDIR /app
COPY . /app
RUN npm install

VOLUME /app

EXPOSE 3000

CMD [ "/usr/local/bin/npm", "run", "dev" ]
