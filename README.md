# Landscape measures for fragmentation/connectivity

## Description
The repository contains python scripts to calculate a number of landscape measures used as indicators of fragmentation and/or connectivity of land cover or habitat classes in the selected study area. In particular, the following measures are calculated:
* percentage of landscape (PLAND);
* patch density (PD);
* shape index distribution (SHAPE);
* total class area (CA); and
* mean patch size (MPS);
* effective mesh size (MESH);
* area-weighted mean patch fractal dimension (AWMPFD).

The selected class- and landscape-level measures are calculated in a cell basis, 
to provide more localized information. A squared-shape moving cell is employed
to calculate local values of each measure, for each land cover or habitat class.
Further details on the methodology can be found in Petrou et al. (2013) whereas
on the selected measures in McGarigal (2015) and Mairota et al. (2013).

The algorithm is implemented in a way to be executed in a Sandbox Virtual Machine (VM) framework provided by [Terradue](https://www.terradue.com/), taking advantage of the parallel processing the platform offers.

#### References
* Mairota, P., Cafarelli, B., Boccaccio, L., Leronni, V., Labadessa, R., Kosmidou, V., Nagendra, H., 2013. Using landscape structure to develop quantitative baselines for protected area monitoring. Ecol. Ind. 33, 82–95.
* McGarigal, K. 2015. FRAGSTATS help. Accessed 31 January 2016. http://www.umass.edu/landeco/research/fragstats/documents/fragstats.help.4.2.pdf.
* Petrou, Z.I., Manakos, I., Kosmidou, V., Lucas, R., Adamo, P., Tarantino, C., Blonda, P., 2013. Indicator extraction software. FP7 project BIO_SOS, Deliverable 6.12.

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
   ```
* Install the scripts
   ```bash
   cd ECOPOTENTIAL-WP6
   mvn clean install
   ```


===============================

## Run the scripts
To run the scripts with the default parameters and input, after installing 
them in the Sanbox as described above, simply run
```bash
ciop-simjob my_node
```

To set different parameters and/or input files, the following need to be performed.

1. Set the size of the moving cell and the step distance between consecutive
cells
   * Open the application.xml file under ECOPOTENTIAL-WP6/scr/main/app-resources/ and update the values of "cellSize" and "step" in lines within the "jobTemplates" section. The values are expressed in meters and the default ones are '1000' for the cell size and '500' for the step. 

2. Set the sources of the input files.
  
  
      ```bash
      cd
      cd ECOPOTENTIAL-WP6/
