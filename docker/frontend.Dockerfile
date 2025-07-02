# Use Node.js 18 Alpine for smaller size
FROM node:18-alpine

# Install dependencies
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED=1

# Build the application
RUN npm run build

# Expose port
EXPOSE 4000

# Set environment variables
ENV PORT=4000
ENV HOSTNAME="0.0.0.0"

# Start the application
CMD ["npm", "start"] 