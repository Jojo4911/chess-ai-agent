# Stage 1 : build Angular
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --prefer-offline
COPY . .
RUN npx ng build --configuration production

# Stage 2 : servir avec nginx
FROM nginx:1.27-alpine
# Adapter le chemin si angular.json indique un nom différent
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80