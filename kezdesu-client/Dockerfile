# Используем Node.js
FROM node:20-alpine

# Создаём рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект
COPY . .

# Экспонируем порт (тот, что использует react-scripts start)
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "start"]
