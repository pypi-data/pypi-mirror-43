# dst-server-deploy
A Python package for generating server files for use with [Don't Starve Together Docker Images](https://github.com/fairplay-zone/docker-dontstarvetogether).

The image requires docker engine and docker compose to be installed on the host system. 

This script is indended to be run in the directory in which you want to store the server data to generate most generic servers. 
If you need to tune the server after generation, look [here](https://github.com/fairplay-zone/docker-dontstarvetogether/blob/develop/docs/configuration.md) for reference.

## How to use
### Package Installation
```console
pip install dst-server-deploy
```

### Build Server Files
```console
dst-server-deploy
```

#### Notes
* Cli arguments may be used to bypass the full questionnaire (See `-h` flag for more information)
* The script assumes you are running a single world (forest + caves) on your machine. If you are running multiple servers, you will need to adjust ports accordingly.

### Deploy Server (requires docker engine and docker-compose)
```console
docker-compose up -d
```

# Reference files.
For an example of the files which may be read into the script, look [here](/reference_files/).

## Contribution
Do you want to contribute to the project? Check out the [contribution guide](/CONTRIBUTING.md).
