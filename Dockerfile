# Use an official Python runtime as a parent image
FROM python:3.13.1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 5000 available to the world outside the container
EXPOSE 5000

# Run flask db upgrade and then python app.py when the container launches
CMD ["sh", "-c", "flask db upgrade && python3 app.py"]

# 1. Build the Docker image
# Command: docker build -t calisthenics-blog .

# 2. List all running containers (to find container ID or name)
# Command: docker ps

# 3. Stop a running container (replace <container_id_or_name> with actual ID or name)
# Command: docker stop <container_id_or_name>

# 4. Remove a stopped container (replace <container_id_or_name> with actual ID or name)
# Command: docker rm <container_id_or_name>

# 5. List all images (to find image ID or name)
# Command: docker images

# 6. Remove the Docker image (replace calisophy with image ID or name)
# Command: docker rmi calisthenics-blog

# 7. Run a new container in detached mode (replace calisophy with image name)
# Command: docker run -p 5000:5000 -d --name calisthenics-blog-container calisthenics-blog