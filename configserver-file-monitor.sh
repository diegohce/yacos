#!/bin/bash



CONFIGSERVER="katara.olleros/configserver"
USERNAME="dodeploy"
PASSWORD="deployonly!"
ENVIRONMENT="PROD"

LOCAL_FILE="$1"
REMOTE_TEMPLATE="$2"


URL="http://$CONFIGSERVER/config/download/$ENVIRONMENT/$REMOTE_TEMPLATE"


wget --http-user="$USERNAME" --http-password="$PASSWORD" "$URL"  -o /dev/null -O ./temporary.file

local_crc=$(crc32 "$LOCAL_FILE") 


remote_crc=$(crc32 ./temporary.file)

if [ "$local_crc" != "$remote_crc" ] ; then
	echo "Remote and local are not the same"
	exit 1	
fi



