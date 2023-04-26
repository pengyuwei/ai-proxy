#!/bin/sh
export YELLOW='\033[33m'
export C='\033[33m'
export N='\033[0m'
export API='https://127.0.0.1:9090/api/v1.0'
export TYPE_TEXT='text/plain'
export TYPE_JSON='Content-Type:application/json'
export TYPE_FORM="application/x-www-form-urlencoded"
export TOKEN='ABCDEF0123456789'
export HEADER_TOKEN="Authorization:$TOKEN"

echo "\nPOST $C/ai$N"
curl -X POST -H $HEADER_TOKEN -H $TYPE_JSON -d '{"question":"太阳表面温度是多少?"}' $API'/ai'

echo "\nGET $C/ai$N"
curl -X GET -H $HEADER_TOKEN -H $TYPE_JSON $API'/ai/太阳表面温度是多少?'
echo $?
