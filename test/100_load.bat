@echo off
rem Send a minor payload of 100 requests to the load balancer for server distribution

FOR /L %%i IN (1,1,100) DO (
    echo Sending request with request_id=%%i
    curl http://localhost:5000/request?request_id=%%i
)
pause
