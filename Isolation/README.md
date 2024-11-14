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

-   `docker pull isepdei/insecurelabs01:latest`
-   `docker run -it isepdei/insecurelabs01:latest /bin/sh`
-   `cat .env`

Additionally, we can simply copy the contents of the .env file to a new file for further inspection. To do this, locate the container ID of the running container and then copy the file from the container to our local system:

-   `docker ps`
-   `docker cp <container_id>:/app/.env <local_path>/.env `

After executing these commands, we can review the contents of the .env file.

### Question 3

The change to the Dockerfile in which Tom removes the `.env` file after the yarn install step is an attempt to prevent the `.env` file from remaining in the final image.
However, each command in a Dockerfile creates a new layer in the image. When the `.env` file is copied into the image and subsequently removed, it is still present in the previous layers. This means anyone with access to the Docker image can retrieve the `.env` file by inspecting the image’s layer history.

### Question 4

In order to recover the new api key, we made use again of the `dive` tool.
As seen in the following figure, the `.env` file is added to the image in layer with digest `sha256:dbe6f4e6fd9843a235b3c1f548841df0519851502bae1c70636e51e911d977d5`.
![dive analysis on insecure2](images/dive-insecure2.jpg)

We can save the multiple image layers to a `tar` file using the `docker save` command:

-   `docker save -o insecurelabs2.tar  isepdei/insecurelabs02:latest`

After that, we can use the `tar` tool again to extract the contents into a folder:

-   `tar -tvf insecurelabs2.tar`

![insecure2 layers](images/insecure2Layers.jpg)

Analyzing the multiple file inside `/blobs/sha256` we can right away identify layer `dbe6f4e6fd9843a235b3c1f548841df0519851502bae1c70636e51e911d977d5`, corresponding to the information `dive` gave us.

Among other information inside this specific file, we can see the secrets Tom tried to protect:

-   `API_KEY=7b5539b2-f0e2-4302-803f-c95289c7f0d7`
-   `USER=jdsl`

### Question 5

In order to use environment variables in docker, we have a few options:

-   We could specify them with the `-e` flag or with an `.env` file:
    -   `docker run -e API_KEY=xxxx -e USER=tom isepdei/insecurelabs01:latest`
    -   `docker run --env-file .env -p 3000:3000 insecurelabs01:latest`
-   Use docker secrets (If using Docker Swarm or Kubernetes):
-   use external secrets management solutions like AWS Secrets Manager or HashiCorp Vault

### Question 6

In order to remove the `cap_net_raw` capability from the `ping` command, we issued the command:

-   `sudo setcap cap_net_raw-ep /usr/bin/ping`

After this operation, trying to execute a ping command resulted in the following error:

-   `ping: => missing cap_net_raw+p capability or setuid?`
