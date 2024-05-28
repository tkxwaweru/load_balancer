@echo off

rem Dynamically add server 6
curl -X POST -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"6\"]}" http://localhost:5000/add


