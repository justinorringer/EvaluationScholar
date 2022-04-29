FROM node:16

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install --save @toast-ui/chart @toast-ui/react-chart

RUN npm install @mui/material @mui/icons-material @emotion/react @emotion/styled

COPY . .

EXPOSE 3000

CMD ["npm", "start"]