# Use an official Python runtime as a parent image
FROM ubuntu:latest 
# Set the working directory in the container
WORKDIR /app
ARG PYVER="3.9"
ENV TZ=US/Pacific \
    DEBIAN_FRONTEND=noninteractive
ARG GITUN="Adithya Shankar"
ARG GITEMAIL="adithya7shankar@gmail.com"
# Copy the current directory contents into the container at /app
COPY . /app
RUN apt update
RUN apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python$PYVER \
    python3-pip
# Install any needed packages specified in requirements.txt
RUN apt-get install -y git-all
RUN apt install python3-cryptography
ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y python3-matplotlib
RUN apt-get -y upgrade && \
    apt-get install -y python3-pip
RUN git config --global user.name "$GITUN" &&\
    git config --global user.email "$GITEMAIL" &&\
    git config --global init.defaultBranch main
# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "main.py"]

