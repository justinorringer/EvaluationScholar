FROM node:16

WORKDIR /src/frontend

COPY package*.json ./

RUN npm install

COPY . /src/frontend

EXPOSE 3000

CMD ["npm", "start"]