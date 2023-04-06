# FROM node:lts-alpine

# WORKDIR /app

# ENV PATH /app/node_modules/.bin:$PATH

# COPY package.json .
# COPY package-lock.json .

# RUN npm install
# RUN npm install @vue/cli@5.0.8 -g

# CMD ["npm", "run", "serve"]
# этап сборки (build stage)
FROM node:lts-alpine as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .
RUN npm run build

# этап production (production-stage)
FROM nginx:stable-alpine as production-stage
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

ENV NODE_ENV="production"

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
