# BrandChecker App Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ .

# Expose port
EXPOSE 3001

# Start app development server
CMD ["npm", "run", "app:dev", "--", "--host"]
