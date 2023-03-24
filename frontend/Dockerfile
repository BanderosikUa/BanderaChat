FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json .
COPY package-lock.json .

RUN npm install
RUN npm install @vue/cli@5.0.8 -g

CMD ["npm", "run", "serve"]
