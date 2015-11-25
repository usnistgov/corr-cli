#!/bin/bash

# echo `curl -X POST -d @req_create_record1.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/record/push/repro_lab --header "Content-Type:application/json"`

# echo ` curl -X POST -F image=@ddsm-api.tar -d @req_create_record2.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/record/push/repro_lab --header "Content-Type:multipart/form-data"`

# echo `curl -X POST -d @req_create_raw1.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/raw/push/repro_lab --header "Content-Type:application/json"`

# echo `curl -X POST -F image=@ddsm-api.tar -F data=@req_create_raw2.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/raw/push/repro_lab --header "Content-Type:multipart/form-data"`

# echo `curl -X POST -F image=@ddsm-api.tar -F data=@req_create_raw2.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/raw/push/repro_lab --header "Content-Type:multipart/form-data"`

# echo `curl -X POST -F image=@ddsm-api.tar -F data=@req_create_raw2.json http://127.0.0.1:5100/api/v1/abcdefghijklmnopqrst0123456789/raw/push/sample1 --header "Content-Type:multipart/form-data"`


# echo `curl -v -O -J http://127.0.0.1:5100/api/v1/public/552e852fcdca246330f2bb06/record/pull/sample1/553519973a90682681a76863`

# echo `curl -X POST -d @req_create_record1.json http://127.0.0.1:5100/api/v1/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/record/push/repro_lab --header "Content-Type:application/json"`

# echo `curl -X DELETE http://127.0.0.1:5100/api/v1/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/record/remove/sample1/558324c19f9d516941d11dea --header "Content-Type:application/json"`

# echo `curl -X POST -d @req_create_record1.json http://127.0.0.1:5100/api/v1/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/record/push/repro_lab --header "Content-Type:application/json"`

# echo `curl -X GET http://127.0.0.1:5100/api/v1/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/record/display/sample1/558333719f9d516e1a800778 --header "Content-Type:application/json"`

echo `curl -X PUT -d @req_sync_record.json http://127.0.0.1:5100/api/v1/3a8d4cc793bd3e5b85c733b523584545991ea74ebe91ff51c7945e10bdc97e40/record/sync/repro_lab/55833be59f9d516e1a800779 --header "Content-Type:application/json"`
