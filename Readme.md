# Adjust .env

cp app/.env-sample  /app/.env

# Run Client to test
python client.py

# Docker
pip freeze > requirements.txt
docker build -t my_flask_app .
docker run -p 5000:5000 my_flask_app
