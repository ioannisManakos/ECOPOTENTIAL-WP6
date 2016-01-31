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
The following steps need to be followed to install the software in a Sandbox VM.

* Log on your Developer Cloud Sandbox host
* Install python in the VM, typing the following commands in the VM terminal:
```bash
sudo yum install -y miniconda-3.8.3
export PATH=/opt/anaconda/bin:$PATH
sudo conda update python
sudo conda install cioppy
```
* Install the required python modules, such as
```bash
sudo conda install numpy
sudo conda install scikit-image
sudo conda install gdal
```
* Copy the GitHub repository in your local VM
```bash
cd
git clone https://github.com/ioannisManakos/ECOPOTENTIAL-WP6.git
cd ECOPOTENTIAL-WP6
mvn clean install
```

===============================

## Run the scripts
