# Aplicativo-Costos

primero crear el estorno virtual si es que no se ah creado

python -m venv .venv

.venv\Scripts\activate

segundo instalar las dependencias en el archivo txt requerimentst.txt 

pip install -r requirements.txt

Si se requiere actualizar las versiones de las dependencias, volver a reinstalar las depeendencias con 

pip install --force-reinstall -r requirements.txt

Cuestion de Docker

para construir la imagen usar esta imagen 

docker build -t backend-app .

para ejecutarla

docker run -p 5000:5000 backend-app
