@echo off
setlocal enabledelayedexpansion

rem Step 1: Remove server 1 to simulate failure of the server and inability to handle requests
echo Removing server 1...
curl -X DELETE -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"1\"]}" http://localhost:5000/rm 
timeout /t 5

rem Step 2: Add server 4 - new replica to handle load
echo Adding server 4...
curl -X POST -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"4\"]}" http://localhost:5000/add
timeout /t 5

rem Step 3: Display active replicas
echo Displaying active replicas...
curl http://localhost:5000/rep
timeout /t 5

rem Step 4: Send a payload of 1000 requests for testing
echo Sending a payload of 1000 requests...
FOR /L %%i IN (1,1,1000) DO (
    echo Sending request with request_id=%%i
    curl http://localhost:5000/request?request_id=%%i
)
timeout /t 5

rem Step 5: Display count of requests per active server
echo Displaying count of requests per server...
rem Define the base URL
set BASE_URL=http://localhost:5000

rem Define the active servers (update this list as needed)
set ACTIVE_SERVERS=2 3 4 

rem Temporary file to store curl output
set TEMP_FILE=temp_output.txt

rem Iterate over each server and get the requests
for %%s in (%ACTIVE_SERVERS%) do (
    rem Fetch the requests for the current server and save to temporary file
    curl %BASE_URL%/requests/%%s > %TEMP_FILE%

    rem Count the number of request IDs
    set COUNT=0
    for /f %%A in ('findstr /r /c:"[0-9]" %TEMP_FILE% ^| find /c /v ""') do (
        set COUNT=%%A
    )

    rem Display the count
    echo Number of requests for Server %%s: !COUNT!
    echo.
)

rem Clean up the temporary file
del %TEMP_FILE%

endlocal
