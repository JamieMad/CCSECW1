FROM node:lts-alpine AS build

WORKDIR /app

COPY ./react/my-app/package*.json ./

RUN npm install

COPY ./react/my-app/src ./src

COPY ./react/my-app/public ./public

RUN npm run build

FROM nginx:stable-alpine AS production

COPY --from=build /app/build /usr/share/nginx/html
COPY ./react/my-app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]