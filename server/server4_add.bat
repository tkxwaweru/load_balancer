@echo off

rem Dynamically add server 4
curl -X POST -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"4\"]}" http://localhost:5000/add


