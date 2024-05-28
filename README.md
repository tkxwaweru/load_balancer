<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">

# IMPLEMENTING A LOAD BALANCER 

## Quick Links
- [Introduction]()

- [Project installation]()

- [Running the project]()

  1. [Creating the server]()

  2. [Implementation of consistent hashing]()

  3. [Implementation of the load balancer]()

- [Analysis]()

## Introduction

## Running the project

### 1. Creating the server
### 2. Implementation of consistent hashing
### 3. Implementation of the load balancer

## Analysis

### 1. Test 1: Request handling on N = 3 server containers
Launch 10000 async requests on N = 3 server containers and report the request count handled by each server instance in a bar chart. Explain your observations in the graph and your view on the performance.
### 2. Test 2: Request handling while incrementing server containers from N = 2 to N = 6
Next, increment N from 2 to 6 and launch 10000 requests on each such increment. Report the average load of the servers at each run in a line chart. Explain your observations in the graph and your view on the scalability of the load balancer implementation.
### 3. Test 3: Testing of endpoints and server failure handling
Test all endpoints of the load balancer and show that in case of server failure, the load balancer spawns a new instance quickly to handle the load.
### 4. Hash function modification
Finally, modify the hash functions H(i), Φ(i, j) and report the observations from Test 1 and Test 2.