# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application's source code
COPY . .

# Build the application for production
RUN npm run build

# Install a simple server to serve the static files
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 5173

# Define the command to run the app
CMD [ "serve", "-s", "dist", "-l", "5173" ]