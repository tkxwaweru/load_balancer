@echo off

rem Display a count of the number of request distributed to and handled by each server replica
setlocal enabledelayedexpansion

rem Define the base URL
set BASE_URL=http://localhost:5000

rem Define the active servers (update this list as needed)
set ACTIVE_SERVERS=1 2 3 4 5 6

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
