FROM node:22-alpine

WORKDIR /frontend

COPY . .

RUN npm ci && npm run build && npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]
