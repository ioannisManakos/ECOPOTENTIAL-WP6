# Landscape measures for fragmentation/connectivity

## Description
The repository contains python scripts that demonstrate the use of parallel processing with a Sandbox Virtual Machine (VM) framework provided by [Terradue](https://www.terradue.com/). The scripts calculate a number of landscape measures used as indicators of fragmentation and/or connectivity of land cover or habitat classes in the selected study area. In particular, the following measures are calculated:
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
Open the application.xml file under ECOPOTENTIAL-WP6/scr/main/app-resources/ and update the values of "cellSize" and "step" in lines within the "jobTemplates" section:
      ```bash
      <parameter id="cellSize">1000</parameter>
      <parameter id="step">500</parameter>
      ```
The values are expressed in meters and the default ones are '1000' for the cell size and '500' for the step. 

2. Set the sources of the input files.
Two geospatial raster files of a selected study area are used as input to the algorithm, in particular:
* A land cover or habitat classification file, where each pixel contains a numerical id value indicating the class it belongs;
* A segmentation file, where each pixel contains the numerical id of the object/segment/patch of the area it belongs in.
The geospatial files used as input are currently downloaded from a dropbox repository, as compressed .zip file. The urls which the data are downlowaded from are stored in a 'list' file under ECOPOTENTIAL-WP6/src/main/app-resources/inputs/. Alternatively, the input files can be read from an online catalogue repository or retrieved from the VM local temporary /tmp folder (assuming they have been previously stored there). Further details on the different options to define input files can be found [here](http://docs.terradue.com/developer-sandbox/reference/application/index.html#application-descriptor-values-and-properties).

To change the source of the input files, the following line within the "workflow" section in the application.xml file needs to be updated:
      ```bash
      <source refid="file:urls">/application/inputs/list</source>
      ```
Currently, a habitat classification and a segmentation file are provided for each of two selected study areas, in order to demonstrate the Sandbox VM capability for parallel processing (one node processing the data for each study area). The 'list' file would look like:
```bash
https://dl.dropboxusercontent.com/u/6489496/LeCesine_Classes.zip*****https://dl.dropboxusercontent.com/u/6489496/LeCesine_Objects.zip
https://dl.dropboxusercontent.com/u/6489496/LagoSalso_Classes.zip*****https://dl.dropboxusercontent.com/u/6489496/LagoSalso_Objects.zip
```
The first line indicates the urls where the classification and object files can be retrieved from. The files are separated by five asterisk symbols '*****', as convention for the algorithm to understand the existence of two input files at the same node (they both are at the same line). The second line includes the urls of the respective files for the second study area. Note: No empty line should exist in the 'list' file.

3. After editing the input parameters and files, re-install the scripts
```bash
cd
cd ECOPOTENTIAL-WP6
mvn clean install
```

4. Run the scripts to calculate the landscape measures
```bash
ciop-simjob my_node
```

5. To inspect the output messages and debug the workflow if needed, copy the "Tracking URL" found in the output of the ciop-simjob command, open a browser and paste the Tracking URL just copied. You may follow an approach similar to the one described [here](http://docs.terradue.com/developer-sandbox/developer/debug.html).

6. To inspect and download the produced (and published) outputs locally, follow a process similar to the one described [here](http://docs.terradue.com/developer-sandbox/developer/browseresults.html). In particular, for the particular scripts, the process should be:
* Retrieve the $HOSTNAME value
```bash
echo $HOSTNAME
```
* Open a browser and type:
```bash
http://$HOSTNAME:50070
```
* Click on the link Browse the filesystem,
* Click on the link ciop,
* Click on the link run,
* Click on the link hands-on-8,
* Click on the link representing the workflow id (e.g., 0000269-150209145053100-oozie-oozi-W),
* Click on the link _result,
* To see intermediate results, click on node_expression and then click on data.
