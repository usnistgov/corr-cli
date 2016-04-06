#!/bin/bash

#Add the dockerfile and requirements through json data.
# rm -rf Dockerfile
# rm -rf requirements.txt
# curl -X POST -d @req_create_project1.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/project/push/sample1 --header "Content-Type:application/json" > docker.tar
# tar -xvzf docker.tar
# rm docker.tar

#Upload the dockerfile and requirements
# curl -X POST -F requirements=@requirements.txt -F dockerfile=@Dockerfile http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/project/push/repro_lab --header "Content-Type:multipart/form-data" > docker.tar
# rm -rf Dockerfile
# rm -rf requirements.txt
# tar -xvzf docker.tar
# rm docker.tar


#Build the docker image
#Export the docker image to a tar file
#Create sync endpoint to upload the docker image
#Add some fields in the record and the project (status, ...) to describe repeatability, reproducibility.
#Maybe the dockerfile should be built at each record and pushed.
#/record/dockerize/project_name

# rm -rf docker.tar
# echo `curl -v -O -J http://127.0.0.1:5100/api/v1/public/552e852fcdca246330f2bb06/project/pull/sample1`

# echo `curl -X POST -d @req_create_project1.json http://127.0.0.1:5100/api/v1/private/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/project/push/repro_lab --header "Content-Type:application/json"`


# echo `curl -X POST -F data=@req_sync_project.json -F image=@docker.tar http://127.0.0.1:5100/api/v1/private/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/project/sync/repro_lab --header "Content-Type:multipart/form-data"`

echo `curl -X GET http://10.0.0.184:5100/api/v1/private/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/project/remove/demo-sumatra --header "Content-Type:application/json"`

# echo `curl -X PUT -d @req_create_project1.json http://127.0.0.1:5100/api/private/v1/2d122c967790c10ad76d21be852c3775c622e97632390b0935be8effdf38dca9/project/sync/sample1 --header "Content-Type:application/json"`

# echo `curl -X GET http://127.0.0.1:5100/api/v1/private/2d122c967790c10ad76d21be852c3775c622e97632390b0935be8effdf38dca9/project/pull/sample1 --header "Content-Type:application/json"`

