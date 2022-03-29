FROM node:16

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install --save @toast-ui/chart

COPY . .

EXPOSE 3000

CMD ["npm", "start"]