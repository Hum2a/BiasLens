# Dockerfile for Next.js
FROM node:16

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy project files
COPY . .

# Build Next.js app
RUN npm run build

# Expose port and start app
EXPOSE 3000
CMD ["npm", "run", "start"]
