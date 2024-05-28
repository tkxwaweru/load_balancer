@echo off
rem Send a payload of 10000 asynchronous requests to the load balancer for server distribution

FOR /L %%i IN (1,1,10000) DO (
    echo Sending request with request_id=%%i
    curl http://localhost:5000/request?request_id=%%i
)
pause
