FROM node:lts-alpine

WORKDIR /app

ENV HOST=0.0.0.0
ENV PATH /app/node_modules/.bin:$PATH

RUN npm install @vue/cli@5.0.8 -g

COPY package.json .
COPY package-lock.json .
RUN npm install

# CMD ["npm", "run", "dev"]