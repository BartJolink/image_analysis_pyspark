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
2. Run the docker containr using the command:   
`docker run -it --rm --mount type=bind,source=./image_analysis_pyspark,target=/image_analysis bartjj/pyspark_image_analysis:latest /bin/bash`
    * For `source=./image_analysis_pyspark`, use the full path to the directory (the cloned repository).    
      *e.g. `source=/mnt/d/project/image_analysis_pyspark`*
3. Run script:   
 `python3 pyspark_ml.py main`

# Results
The top 5 rows of the table of raw predictions

|       rawPrediction|prediction|label|            features|
---------------------|----------|-----|--------------------|
| 2.30111863728145...|       0.0|NO_SP| 1.9,1.8,-1.6,-0....|
| 2.30111863728145...|       0.0|NO_SP|[1.9,-3.5,2.8,-0....|
| 2.30111863728145...|       0.0|NO_SP|[1.9,-3.5,-3.5,4....|
| 2.30111863728145...|       0.0|NO_SP|[1.9,3.8,-0.4,-0....|
| 2.30111863728145...|       0.0|NO_SP|[1.9,3.8,-0.4,1.8...|

The test accuracy:
 `74.55465784094227%`

The test error: 
 `25.445342159057727%`
