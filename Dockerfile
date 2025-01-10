FROM python:3.13.1
# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container's working directory
COPY . .

# Install dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Set the command to run the Python application
CMD flask db upgrade && python3 app.py

# 1. Build the Docker image
# Command: docker build -t calisophy .

# 2. List all running containers (to find container ID or name)
# Command: docker ps

# 3. Stop a running container (replace <container_id_or_name> with actual ID or name)
# Command: docker stop <container_id_or_name>

# 4. Remove a stopped container (replace <container_id_or_name> with actual ID or name)
# Command: docker rm <container_id_or_name>

# 5. List all images (to find image ID or name)
# Command: docker images

# 6. Remove the Docker image (replace calisophy with image ID or name)
# Command: docker rmi calisophy

# 7. Run a new container in detached mode (replace calisophy with image name)
# Command: docker run -d --name calisophy-container calisophy