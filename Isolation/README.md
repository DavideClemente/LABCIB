## Part 1: Keeping Secrets OUT of Docker Images

### Question 1

When the .env file is copied into the image (using COPY . .), it becomes part of a Docker layer. Even if you delete the .env file in a later layer, Docker images maintain each layer in the image history, which means the sensitive information could still be extracted by anyone with access to the image.

### Question 2

Using the tool [dive](https://github.com/wagoodman/dive) we can observe that the docker image contains the `.env` file within its layers.
![InsecureLabs01](images/dive-insecure1.jpg)

In order to retrieve the contents of the `.env` file, we can create a temporary container from the image and then use the `docker export` command to export its contents to a `.tar` file:

-   `docker create --name insecure1_temp isepdei/insecurelabs01:latest`
-   `docker export insecure1_temp -o insecure1.tar`

After creating the tar file, we can use the `tar` cli tool to decompress the contents into a regular folder.

-   `mkdir insecure1`
-   `tar -xvf insecure1.tar -C insecure1`

Navigating inside the /app folder, we can already see the `.env` file and it's content
![.env file](images/env_file.jpg)
![.env file content](images/envFileContent.jpg)

An alternative approach is to pull the image and run it in an interactive shell, which allows us to examine the container's environment and potentially explore or test security settings. To do this, run the following commands:

 - `docker pull isepdei/insecurelabs01:latest`
 - `docker run -it isepdei/insecurelabs01:latest /bin/sh`
 - `cat .env`
Additionally, we can simply copy the contents of the .env file to a new file for further inspection. To do this, locate the container ID of the running container and then copy the file from the container to our local system:

 - `docker ps`
 - `docker cp <container_id>:/app/.env <local_path>/.env `
  
After executing these commands, we can review the contents of the .env file.

