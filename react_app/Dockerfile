# Use a base image with Node.js
FROM node:14-alpine

# Set the working directory inside the Docker container
WORKDIR /app

# Copy necessary files
COPY . .

# Install dependencies
RUN npm install

# Build the React app
# RUN npm run build

# Command to start the React app
CMD ["npm", "run", "dev"]
