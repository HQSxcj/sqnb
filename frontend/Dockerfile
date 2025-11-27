FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
EXPOSE 9710  # 确保这里也是 9710

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "9710"]
