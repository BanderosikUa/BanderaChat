# Use a Node.js base image for building the Vue.js application
FROM node:14 as build-stage

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the working directory
COPY . .

# Build the Vue.js application
RUN npm run build

# Use an Nginx base image for serving the built files
FROM nginx:1.21

# Copy the built files from the build-stage to the Nginx default public directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy the Nginx configuration file to the appropriate location
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
