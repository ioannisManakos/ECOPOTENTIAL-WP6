# Landscape measures for fragmentation/connectivity

## About
The repository contains python scripts to calculate a number of landscape measures used as indicators of fragmentation and/or connectivity of land cover or habitat classes in the selected study area. In particular, the following measures are calculated:
* percentage of landscape (PLAND);
* patch density (PD);
* shape index distribution (SHAPE);
* total class area (CA); and
* mean patch size (MPS);
* effective mesh size (MESH);
* area-weighted mean patch fractal dimension (AWMPFD).

The algorithm is implemented in a way to be executed in a Sandbox Virtual Machine (VM) framework provided by [Terradue](https://www.terradue.com/), taking advantage of the parallel processing the platform offers.

=================================

## Installation
The following steps need to be followed to install the software in 
###dfsdfsa
####dfads
fads


=================================

Developer Cloud Sandbox Hands-On Exercises
==========================================

Installation
-------------

* Log on your Developer Cloud Sandbox host

* Install the needed package:

```bash
sudo yum install -y beam-5.0
```

* Run these commands in a shell:

```bash
cd
git clone https://github.com/Terradue/dcs-hands-on.git
cd dcs-hands-on
mvn clean install -D hands.on=-id- -P bash
```

where *-id-* is the identifier of the Hands On you want to install. For example:

```
mvn clean install -D hands.on=1 -P bash
```

Available Hands On
------------------

* [Hands-On Exercise 1: a basic workflow](src/main/app-resources/hands-on-1)
* [Hands-On Exercise 2: make a robust workflow and debug it](src/main/app-resources/hands-on-2)
* [Hands-On Exercise 3: staging data](src/main/app-resources/hands-on-3)
* [Hands-On Exercise 4: using a toolbox](src/main/app-resources/hands-on-4)
* [Hands-On Exercise 5: using parameters](src/main/app-resources/hands-on-5)
* [Hands-On Exercise 6: multi-node workflow](src/main/app-resources/hands-on-6)
* [Hands-On Exercise 7: debug a multi-node workflow](src/main/app-resources/hands-on-7)
* [Hands-On Exercise 8: browse published results](src/main/app-resources/hands-on-8)
* [Hands-On Exercise 9: using an OpenSearch catalogue](src/main/app-resources/hands-on-9)
* [Hands-On Exercise 10: prepare an OGC Web Processing Service](src/main/app-resources/hands-on-10)
