# 1. Imagen base de Node.js
FROM node:20

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /apli

# 3. Crear un package.json con las dependencias esenciales
RUN npm init -y \
    && npm install \
    react \
    react-dom \
    react-router-dom \
    axios \
    vite \
    @vitejs/plugin-react \
    eslint \
    eslint-plugin-react --save

# 4. Copiar todo el código fuente de la aplicación al contenedor
COPY . .

# 5. Exponer el puerto 5173 (Vite)
EXPOSE 5173

# 6. Comando para iniciar la aplicación
CMD ["npm", "run", "dev", "--", "--host"]
