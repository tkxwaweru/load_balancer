@echo off

rem Display a list of all request ids of request handled by particular servers
setlocal enabledelayedexpansion

rem Define the base URL
set BASE_URL=http://localhost:5000

rem Define the active servers (update this list as needed)
set ACTIVE_SERVERS=1 2 3 4 5 6 

rem Iterate over each server and get the requests
for %%s in (%ACTIVE_SERVERS%) do (
    echo Request IDs for Server %%s:
    curl %BASE_URL%/requests/%%s
    echo.
)

endlocal
