# mLib application
## Teammembers
|   teammembers |   studentnumber   |
----------------|--------------------
|   Bart        |  529366           |
|   Pim         |  614906           |
|   Inge        |  617432           |
|   Noah        |   626290          |

## Summary
The docker container is used to run the script.
Because the docker contains the modules necessary for the script it is no longer necessary to manually install the required modules for the python script to work.
The script is used to classify signalpeptides.

## Requirements
### Docker
To download and install Docker, see https://docs.docker.com/
When using a WSL2 system, make sure that Docker is running on WSL2.

# Usage
1. Clone repository
2. Run the docker containr using the command: docker run -it --rm --mount type=bind,source='`Path to folder with code`',target=/image_analysis `Dockername` /bin/bash
3. Run script: python pyspark_ml.py main
