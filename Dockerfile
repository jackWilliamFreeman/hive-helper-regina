FROM python:3.9

# set a directory for the app
WORKDIR /app/

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r Requirements.txt
ENV AM_I_IN_A_DOCKER_CONTAINER Yes


# tell the port number the container should expose
EXPOSE 5000
 
# run the command
CMD ["python", "main.py"]