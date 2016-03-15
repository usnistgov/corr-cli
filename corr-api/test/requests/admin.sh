#!/bin/bash
dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "------------------------- $dt -------------------------" >> admin.txt
# # Raw endpoints
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/stats --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/traffic --header "Content-Type:application/json"` >> admin.txt

# # List all 
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/users --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/apps --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/messages --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/files --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/diffs --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/projects --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/records --header "Content-Type:application/json"` >> admin.txt

# ## Create endpoints req_create_profile2_success
# # Developers
# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_profile2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/create/5665b42c9f9d5157cfdae61f --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_developer1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_profile1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/create/56620d859f9d513814fa072a --header "Content-Type:application/json"` >> admin.txt

# Users
## "apiToken": "4f8bb51d7caea54b36365ab32158f734dfa02e520668bd38e8ec1fe7b92392d0"
## "apiToken": "62633ba90e65279f23d2e93063b5def4c5adee032764611d72979285a12e68a9"

# echo `curl -X POST -d @req_create_user1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_profile2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/create/5666ed939f9d5171fd03a564 --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_user2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_profile1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/create/5666ee079f9d5171fd03a565 --header "Content-Type:application/json"` >> admin.txt

# # Apps
## "token": "3f810d9cc13ced5dca90a9e869767fadf47bfdf7116de205d7ffb682cc1fcbe2"
## "token": "2f30a50f0ab5ac14df341e7b536c0d0ea84c35e7883d44acf0b7b7df87d9e192"

# echo `curl -X POST -d @req_create_app1_success.json http://0.0.0.0:5100/api/v1/private/admin/app/create --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_app2_success.json http://0.0.0.0:5100/api/v1/private/admin/app/create --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_app3_success.json http://0.0.0.0:5100/api/v1/private/admin/app/create --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_app4_success.json http://0.0.0.0:5100/api/v1/private/admin/app/create --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_app5_success.json http://0.0.0.0:5100/api/v1/private/admin/app/create --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_app6_success.json http://0.0.0.0:5100/api/v1/private/admin/app/create --header "Content-Type:application/json"` >> admin.txt

# Projects
# echo `curl -X POST -d @req_create_project1_success.json http://0.0.0.0:5100/api/v1/private/admin/project/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_project2_success.json http://0.0.0.0:5100/api/v1/private/admin/project/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_project3_success.json http://0.0.0.0:5100/api/v1/private/admin/project/create --header "Content-Type:application/json"` >> admin.txt

# Records
## "56672b3a9f9d510b32f53bf2" pymks
## "56672b3a9f9d510b32f53bf3" TGA
## "566735849f9d510bb0e3af0a" IGA
## "56672b3a9f9d510b32f53bf4" FiPy

# echo `curl -X POST -d @req_create_record1_success.json http://0.0.0.0:5100/api/v1/private/admin/record/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_record2_success.json http://0.0.0.0:5100/api/v1/private/admin/record/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_record3_success.json http://0.0.0.0:5100/api/v1/private/admin/record/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_record4_success.json http://0.0.0.0:5100/api/v1/private/admin/record/create --header "Content-Type:application/json"` >> admin.txt

# Messages
# echo `curl -X POST -d @req_create_message1_success.json http://0.0.0.0:5100/api/v1/private/admin/message/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_message2_success.json http://0.0.0.0:5100/api/v1/private/admin/message/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_message3_success.json http://0.0.0.0:5100/api/v1/private/admin/message/create --header "Content-Type:application/json"` >> admin.txt

# Diffs
# echo `curl -X POST -d @req_create_diff1_success.json http://0.0.0.0:5100/api/v1/private/admin/diff/create --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_diff2_success.json http://0.0.0.0:5100/api/v1/private/admin/diff/create --header "Content-Type:application/json"` >> admin.txt


# ## Show endpoints
# # Developers
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/show/56620d859f9d513814fa072a --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/profile/show/56620d859f9d513814fa072a --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/show/5665b42c9f9d5157cfdae61f --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/profile/show/5665b42c9f9d5157cfdae61f --header "Content-Type:application/json"` >> admin.txt

# Users
## "56620d859f9d513814fa072a" Developer1
## "5665b42c9f9d5157cfdae61f" Developer2
## "5666ed939f9d5171fd03a564" User1
## "5666ee079f9d5171fd03a565" User2


# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/show/5666ed939f9d5171fd03a564 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/profile/show/5666ed939f9d5171fd03a564 --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/show/5666ee079f9d5171fd03a565 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/profile/show/5666ee079f9d5171fd03a565 --header "Content-Type:application/json"` >> admin.txt


# #Apps
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/app/show/5665b7a99f9d515e74427b57 --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/app/show/5665bb9e9f9d515fa2b8c93c --header "Content-Type:application/json"` >> admin.txt

# Projects
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/project/show/566728709f9d5109b8de3f91 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/project/show/566728709f9d5109b8de3f92 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/project/show/566728709f9d5109b8de3f93 --header "Content-Type:application/json"` >> admin.txt

# Records
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/record/show/566728709f9d5109b8de3f91 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/record/show/566728709f9d5109b8de3f92 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/record/show/566728709f9d5109b8de3f93 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/record/show/566728709f9d5109b8de3f93 --header "Content-Type:application/json"` >> admin.txt

# Diff
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/diff/show/56684f6e9f9d5146e5ca15d8 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/diff/show/56684f6e9f9d5146e5ca15d9 --header "Content-Type:application/json"` >> admin.txt


## Update endpoints
# Developers
# echo `curl -X POST -d @req_update_profile1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/update/56620d859f9d513814fa072a --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_profile1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/update/5665b42c9f9d5157cfdae61f --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_profile1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/update/5666ed939f9d5171fd03a564 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_profile1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/profile/update/56620d859f9d513814fa072a --header "Content-Type:application/json"` >> admin.txt


# Apps
# echo `curl -X POST -d @req_update_app1_success.json http://0.0.0.0:5100/api/v1/private/admin/app/update/5665b7a99f9d515e74427b57 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_app2_success.json http://0.0.0.0:5100/api/v1/private/admin/app/update/5665bb9e9f9d515fa2b8c93c --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_app3_success.json http://0.0.0.0:5100/api/v1/private/admin/app/update/5665bf419f9d516140e0639e --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_app4_success.json http://0.0.0.0:5100/api/v1/private/admin/app/update/5665bf419f9d516140e063a0 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_update_app5_success.json http://0.0.0.0:5100/api/v1/private/admin/app/update/5665bf429f9d516140e063a2 --header "Content-Type:application/json"` >> admin.txt


## Delete endpoints


## Custom endpoints

# echo `curl -X POST -d @req_create_user1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_user2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer2_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X POST -d @req_create_developer1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_developer1_success.json http://0.0.0.0:5100/api/v1/private/admin/user/login --header "Content-Type:application/json"` >> admin.txt


# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt

# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/token/update/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt

# Developers logout
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/logout/a19aee3eeef4180effa2acc4af3703dbdbfadfe7f650d4c3bb930272c7d6dce7 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/logout/342841c66d59d1b0228a4baf370d3cc0a7a8036788765d04676cef9c7019e4d7 --header "Content-Type:application/json"` >> admin.txt

# Users logout
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/logout/711432a4fbdacceb4425beae1aed4f8e2f807342c44b0c4e14d100a2d22b3d37 --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X GET http://0.0.0.0:5100/api/v1/private/admin/user/logout/065682175acc1863116bf45890bb7f4db89793631d4d6fff13f95f36fadf619e --header "Content-Type:application/json"` >> admin.txt


# echo `curl -X POST -d @req_create_comment1_success.json http://0.0.0.0:5100/api/v1/private/admin/comment/record --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_comment2_success.json http://0.0.0.0:5100/api/v1/private/admin/comment/record --header "Content-Type:application/json"` >> admin.txt
# echo `curl -X POST -d @req_create_comment3_success.json http://0.0.0.0:5100/api/v1/private/admin/comment/project --header "Content-Type:application/json"` >> admin.txt

# 5662125a9f9d513a71abba49

## Files
# profile picture
# http://0.0.0.0:5100/api/v1/private/admin/file/download/5665b4899f9d5157cfdae620

# app logo
# http://0.0.0.0:5100/api/v1/private/admin/app/logo/5665b7a99f9d515e74427b57

# upload a file

# download a file
START_TIME=$SECONDS
# echo `curl -X POST -F file=@pymks-paper-2015.pdf http://127.0.0.1:5100/api/v1/private/admin/file/upload/descriptive/566728709f9d5109b8de3f91 --header "Content-Type:multipart/form-data"` >> admin.txt
# echo `curl -X POST -F file=@reproducibility.pptx http://127.0.0.1:5100/api/v1/private/admin/file/upload/attach/566763079f9d513c979f2fa7 --header "Content-Type:multipart/form-data"` >> admin.txt
echo `curl -X POST -F file=@pymks-paper-2015.pdf http://127.0.0.1:5100/api/v1/private/admin/file/upload/attach-comment/5669aeef9f9d5162d84546bf --header "Content-Type:multipart/form-data"` >> admin.txt

ELAPSED_TIME=$(($SECONDS - $START_TIME)) >> admin.txt
echo "Duration is $ELAPSED_TIME seconde(s)" >> admin.txt

echo "-------------------------         DONE        -------------------------" >> admin.txt