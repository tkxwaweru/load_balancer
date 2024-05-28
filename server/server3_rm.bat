@echo off

rem Dynamically remove server 3
curl -X DELETE -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"3\"]}" http://localhost:5000/rm

