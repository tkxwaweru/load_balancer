@echo off

rem Dynamically add server 5
curl -X POST -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"5\"]}" http://localhost:5000/add


