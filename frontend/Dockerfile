# Stage 1: Build the React application
# Use a specific Node.js version on a lightweight Alpine base image.
# Naming this stage 'build' allows us to reference it later.
FROM node:18-alpine AS build

# Set the working directory inside the container.
WORKDIR /app

# Copy the package manifests. This step leverages Docker's layer caching and
# only re-runs if package.json or package-lock.json change, optimizing builds.
COPY package.json package-lock.json ./

# Install dependencies using 'npm ci' for a clean, deterministic, and fast installation
# based on the lock file. This is more reliable for CI/CD environments.
RUN npm ci

# Copy the rest of the frontend source code into the container.
# This layer is invalidated more frequently, but the expensive 'npm ci' step above is preserved.
COPY . .

# Build the application for production. This script compiles the source code
# and generates a 'dist' directory with static HTML, CSS, and JS assets.
RUN npm run build

# Stage 2: Serve the application with a lightweight Nginx server
# Use a stable, minimal Nginx image for a secure and small production environment.
FROM nginx:stable-alpine

# Copy the custom Nginx configuration to define how the server handles requests,
# including reverse proxying API calls and supporting client-side routing.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy *only* the built static assets from the 'build' stage into the Nginx web root.
# This is the core principle of a multi-stage build, ensuring the final image is minimal.
COPY --from=build /app/dist /usr/share/nginx/html

# Document that the container listens on port 80.
EXPOSE 80

# The command to start Nginx in the foreground, which is the standard
# and required practice for containerized applications.
CMD ["nginx", "-g", "daemon off;"]