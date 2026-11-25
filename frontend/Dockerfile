# 프론트 이미지 (docs/contract.md 2·6·7절)
# 1단계: 빌드
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# 2단계: root가 아닌 nginx(UID 101)로 제공, 포트 8080
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
