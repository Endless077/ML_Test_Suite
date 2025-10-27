# =====================================================
# Dockerfile - React Frontend (Development Mode)
# Base: Node 20 Alpine
# =====================================================

# Environment Image
FROM node:20-alpine AS dev

LABEL maintainer="user"
LABEL project="React Frontend Dev"
LABEL description="Development container for React application."

# Set working directory
WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose React default port
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]
