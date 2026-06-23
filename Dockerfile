# syntax=docker/dockerfile:1

# ===========================
# Stage 1: Build frontend
# ===========================
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# API URL used by the frontend at build time.
# In compose nginx proxies /api to the backend, so relative path works.
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# ===========================
# Stage 2: Serve with nginx
# ===========================
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
