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


# to remove specific container
docker-compose -f docker-compose-chromadb.yml down --rmi all --volumes  --remove-orphans
docker-compose -f docker-compose-frontend.yml down --rmi all --volumes  --remove-orphans
docker-compose -f docker-compose-backend.yml down --rmi all --volumes  --remove-orphans
docker-compose -f docker-compose-ollama.yml down --rmi all --volumes  --remove-orphans
docker-compose -f docker-compose-mysql.yml down --rmi all --volumes  --remove-orphans
