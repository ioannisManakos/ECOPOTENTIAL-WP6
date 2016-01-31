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

