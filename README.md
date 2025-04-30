# DockerImages
1. Exercise 
    Task1: Built a GUI page your choice (Streamlit OR Flask App)
    Task2: Deploy 2 containers  APP and DB (mysql) populate with any 1 OR 2 tables) . APP UI should have the function to display the table in the Database and you are able to see the records, when you click on the table.
    Task3: Built functionality in the app, to import a source file from your local directory to a target directory in your container APP. 


# to remove all contianer 
docker-compose -f docker-compose-frontend.yml -f docker-compose-backend.yml -f docker-compose-mysql.yml -f docker-compose-ollama.yml -f docker-compose-chromadb.yml down --rmi all --volumes  --remove-orphans

# to add all container 
docker-compose -f docker-compose-frontend.yml -f docker-compose-backend.yml -f docker-compose-mysql.yml -f docker-compose-ollama.yml -f docker-compose-chromadb.yml up -d

# to build specific image from scratch
docker-compose -f docker-compose-frontend.yml build --no-cache
docker-compose -f docker-compose-backend.yml build --no-cache
docker-compose -f docker-compose-mysql.yml build --no-cache
docker-compose -f docker-compose-ollama.yml build --no-cache
docker-compose -f docker-compose-chromadb.yml build --no-cache

# to run specific container 

docker-compose -f docker-compose-frontend.yml up -d
docker-compose -f docker-compose-backend.yml up -d
docker-compose -f docker-compose-mysql.yml up -d
docker-compose -f docker-compose-ollama.yml up -d
docker-compose -f docker-compose-chromadb.yml up -d