@echo off

rem Dynamically add server 3
curl -X POST -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"3\"]}" http://localhost:5000/add


