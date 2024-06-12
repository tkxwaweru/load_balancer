<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">

# IMPLEMENTING A LOAD BALANCER 

## ICS 4B
### Group Members:
1. 137931 Trevor Waweru 
2. 140801 Kyla Arunga
3. 138551 Ruweida Ismail
4. 145644 Fardowsa Hassan

## Quick Links
- [Introduction](https://github.com/tkxwaweru/load_balancer?tab=readme-ov-file#introduction)

- [Running the project](https://github.com/tkxwaweru/load_balancer?tab=readme-ov-file#running-the-project)

- [Analysis](https://github.com/tkxwaweru/load_balancer?tab=readme-ov-file#analysis)

## Introduction
This project deals with the implementation of a load balancer that is meant to divide a load of requests among N server replicas (for instance N = 3 replicas). The purpose of the load balancer is to prevent overwhelming a single server with a large number of requests which could lead to slow server responses and probable server failure.

The system is capable of adding server replicas into the environment to increase the number servers the load balancer has to work with in terms of load distribution. The system utilizes consistent hashing and quadratic probing to guide the load distribution algorithm. 

## Running the project
### 1. Requirements:
1. Windows OS (Windows 10 or newer)
2. Docker version 26.1.1
3. Docker Compose version v2.27.0
4. Python version 3.11.0 or newer
5. Flask version 3.0.3 or newer
6. Docker desktop

### 2. Installation

<b>Disclaimer</b>: Modify the commands appropriately for your case.

1. Clone this repository into your machine 
  ```{code}
  git clone https://github.com/tkxwaweru/load_balancer.git load_balancer
  ```
2. Build the server containers:
  ```{code}
  docker-compose build
  ```
3. Run the containers in the background:
  ```{code}
  docker-compose up -d
  ```
4. View the logs (you can also monitor the logs via docker desktop):
  ```{code}
  docker-compose logs
  ```
5. The system makes use of batch files (.bat) to ease certain operations within the system. They shall be discussed in the analysis section.
## Analysis

### Test 1: Request handling on N = 3 server containers
Launch 10000 async requests on N = 3 server containers and report the request count handled by each server instance in a bar chart. Explain your observations in the graph and your view on the performance.

#### <u>Process</u>
By default, the system starts with N = 3 active server replicas:
```
C:\Users\user\load_balancer\server>replicas.bat
{
  "message": {
    "N": 3,
    "replicas": [
      "1",
      "2",
      "3"
    ]
  },
  "status": "successful"
}
```
To perform this task we utilised a batch file: 10K_load.bat which makes use of the request load balancer endpoint.
```
@echo off
rem Send a payload of 10000 asynchronous requests to the load balancer for server distribution

FOR /L %%i IN (1,1,10000) DO (
    echo Sending request with request_id=%%i
    curl http://localhost:5000/request?request_id=%%i
)
pause
```
After performing this task we used a batch file (request_count.bat) to count requests handled by each of the 3 server replicas then plotted a bar graph showing request count per server.

After running request_count.bat:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 36136  100 36136    0     0   550k      0 --:--:-- --:--:-- --:--:--  551k
Number of requests for Server 1: 3650

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 33801  100 33801    0     0   280k      0 --:--:-- --:--:-- --:--:--  282k
Number of requests for Server 2: 3412

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 29104  100 29104    0     0  1032k      0 --:--:-- --:--:-- --:--:-- 1052k
Number of requests for Server 3: 2938
```
Bar graph:

![Bar graph](https://github.com/tkxwaweru/load_balancer/blob/main/images/test1_bar-graph.png)

<i>Further information on the plotting of the graph can be found in <b>sheets/Analysis.xlsx</b>.</i>

#### <u>Observations</u>

The distribution of requests among the servers seems relatively balanced. Although the numbers aren't exactly equal, they are in the same ballpark, indicating that the load balancer is distributing requests somewhat evenly across the servers.

Overall, based on the observations, the load balancer seems to be performing reasonably well in distributing the load among the available servers.

### Test 2: Request handling while incrementing server containers from N = 2 to N = 6
Next, increment N from 2 to 6 and launch 10000 requests on each such increment. Report the average load of the servers at each run in a line chart. Explain your observations in the graph and your view on the scalability of the load balancer implementation.

#### <u>Process</u>

This test involved a repetititive process of sending a payload of 10000 request to N servers to observe the load distribution starting from N = 2 to N = 6 server replicas. 

This process involved the use of various batch files to add servers dynamically into the system (server3_add.bat, server4_add.bat etc.) a batch file to send the load (10K_load.bat) and finally a batch file to view the load count after each iteration (request_count.bat).

Here is the output from each iteration after running request_count.bat:

1. N = 2:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 53543  100 53543    0     0  1200k      0 --:--:-- --:--:-- --:--:-- 1216k
Number of requests for Server 1: 5412

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 45449  100 45449    0     0   723k      0 --:--:-- --:--:-- --:--:--  727k
Number of requests for Server 2: 4588

```
2. N = 3:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 36136  100 36136    0     0  1012k      0 --:--:-- --:--:-- --:--:-- 1037k
Number of requests for Server 1: 3650

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 33801  100 33801    0     0  1092k      0 --:--:-- --:--:-- --:--:-- 1100k
Number of requests for Server 2: 3412

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 29104  100 29104    0     0  1069k      0 --:--:-- --:--:-- --:--:-- 1093k
Number of requests for Server 3: 2938
```
3. N = 4:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 25802  100 25802    0     0   768k      0 --:--:-- --:--:-- --:--:--  787k
Number of requests for Server 1: 2605

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 25652  100 25652    0     0   948k      0 --:--:-- --:--:-- --:--:--  963k
Number of requests for Server 2: 2588

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 21528  100 21528    0     0   353k      0 --:--:-- --:--:-- --:--:--  356k
Number of requests for Server 3: 2171

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 26108  100 26108    0     0   893k      0 --:--:-- --:--:-- --:--:--  910k
Number of requests for Server 4: 2636

```
4. N = 5:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 21287  100 21287    0     0   491k      0 --:--:-- --:--:-- --:--:--  494k
Number of requests for Server 1: 2148

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 20851  100 20851    0     0   609k      0 --:--:-- --:--:-- --:--:--  617k
Number of requests for Server 2: 2104

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 17592  100 17592    0     0   573k      0 --:--:-- --:--:-- --:--:--  592k
Number of requests for Server 3: 1773

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 19597  100 19597    0     0   702k      0 --:--:-- --:--:-- --:--:--  708k
Number of requests for Server 4: 1976

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 19812  100 19812    0     0   391k      0 --:--:-- --:--:-- --:--:--  394k
Number of requests for Server 5: 1999
```
5. N = 6:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 16035  100 16035    0     0   517k      0 --:--:-- --:--:-- --:--:--  521k
Number of requests for Server 1: 1616

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 17774  100 17774    0     0   627k      0 --:--:-- --:--:-- --:--:--  642k
Number of requests for Server 2: 1793

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 15271  100 15271    0     0   462k      0 --:--:-- --:--:-- --:--:--  466k
Number of requests for Server 3: 1538

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 16141  100 16141    0     0   585k      0 --:--:-- --:--:-- --:--:--  606k
Number of requests for Server 4: 1627

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 17444  100 17444    0     0   752k      0 --:--:-- --:--:-- --:--:--  774k
Number of requests for Server 5: 1760

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 16523  100 16523    0     0   303k      0 --:--:-- --:--:-- --:--:--  304k
Number of requests for Server 6: 1666
```

Below is a line graph that shows the trend of average requests per server as we increment N.

![Line graph](https://github.com/tkxwaweru/load_balancer/blob/main/images/test2_line-graph.png)

<i>Further information on the plotting of the graph can be found in <b>sheets/Analysis.xlsx</b>.</i>

#### <u>Observations</u>

As the number of server replicas (N) increases, the average load per server decreases. This trend suggests that the load balancer is effectively distributing the load more evenly as the number of servers increases. This is a positive indication of the load balancer's ability to scale and handle increased traffic by distributing it across a larger number of servers.

The load balancer implementation demonstrates scalability as evidenced by its ability to handle an increasing number of server replicas while maintaining a balanced load distribution. As N increases from 2 to 6, the average load per server decreases proportionally, indicating that the load balancer can efficiently utilize additional server resources to accommodate higher traffic loads.

### Test 3: Testing of endpoints and server failure handling
Test all endpoints of the load balancer and show that in case of server failure, the load balancer spawns a new instance quickly to handle the load.

1. /rep endpoint:

Here we can make use of the replicas.bat file to demonstrate the functionality of this endpoint:

replicas.bat
```
@echo off
rem Display available replicas of servers in the system

curl http://localhost:5000/rep
```

Sample output:
```
{
  "message": {
    "N": 3,
    "replicas": [
      "2",
      "3",
      "4"
    ]
  },
  "status": "successful"
}
```

2. /rm endpoint:

Here we can make use of a server removal batch file (server3_rm.bat) to demonstrate the functionality of this endpoint by removing server 3:

server3_rm.bat
```
@echo off

rem Dynamically remove server 3
curl -X DELETE -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"3\"]}" http://localhost:5000/rm
```

Output:
```
{
  "message": {
    "N": 2,
    "replicas": [
      "2",
      "4"
    ]
  },
  "status": "successful"
}
```

3. /add endpoint:

Here we can make use of a server addition batch file (server3_add.bat) to demonstrate the functionality of this endpoint by adding server 3 back which we removed above:

server3_add.bat
```
@echo off

rem Dynamically add server 3
curl -X POST -H "Content-Type: application/json" -d "{\"n\": 1, \"hostnames\": [\"3\"]}" http://localhost:5000/add
```

Sample output:
```
{
  "message": {
    "N": 3,
    "replicas": [
      "2",
      "4",
      "3"
    ]
  },
  "status": "successful"
}
```

4. /request endpoint:
The functionality of this endpoint can be demonstrated using the payload batch files e.g. 100_load.bat which make use of the endpoint to send requests to the load balancer for distribution to server replicas.

100_load.bat
```
@echo off
rem Send a minor payload of 100 requests to the load balancer for server distribution

FOR /L %%i IN (1,1,100) DO (
    echo Sending request with request_id=%%i
    curl http://localhost:5000/request?request_id=%%i
)
pause
```

Sample output:
```
Sending request with request_id=1
{
  "response": {
    "message": "Hello from Server: 4",
    "status": "Successful"
  },
  "server_id": "4"
}
Sending request with request_id=2
{
  "response": {
    "message": "Hello from Server: 2",
    "status": "Successful"
  },
  "server_id": "2"
}
Sending request with request_id=3
{
  "response": {
    "message": "Hello from Server: 4",
    "status": "Successful"
  },
  "server_id": "4"
}
```

5. Server failure simulation

Here, a batch file (simulate_failure.bat) is used to simulate the failure of server 1. Upon failure of the server, a new replica, server 4 is added so that we have N = 3 replicas to help distribute the load. The batch file then sends a payload of 1000 request to the 3 replicas and outputs the count of requests per server.

simulate_failure.bat:
```
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
```

Simply run the batch file to observe the simulation:
```
C:\Users\user\load_balancer\server>simulate_failure.bat
```

Load count after simulation:
```
Displaying count of requests per server...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3015  100  3015    0     0  99927      0 --:--:-- --:--:-- --:--:--   98k
Number of requests for Server 2: 333

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2769  100  2769    0     0  28131      0 --:--:-- --:--:-- --:--:-- 28255
Number of requests for Server 3: 306

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3256  100  3256    0     0   109k      0 --:--:-- --:--:-- --:--:--  109k
Number of requests for Server 4: 361
```

### Hash function modification
Finally, modify the hash functions H(i), Φ(i, j) and report the observations from Test 1 and Test 2.

For this case, the load balancer has demonstrated efficiency in load distribution. 

It is capable of nearly evenly distributing load among available server replicas and can continue doing so as the number of replicas increase thus also demonstarting scalability. As such the hashing algorithm need not be modified.

## Conclusion
The load balancer developed has proven successful. It is capable of close to evenly distributing load across available active server replicas. This can be observed in the analysis section. Moreover, the system is capable of managing it's active server replicas through processes such as adding replicas, removing replicas and routing requests to available replicas using a consistent hashing algorithm.
