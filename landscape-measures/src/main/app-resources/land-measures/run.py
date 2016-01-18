#!/opt/anaconda/bin/python

import sys
import os
import math
import re
import numpy as np
#from rios import rat
import osgeo.gdal as gdal
from gdalconst import *
import pymorph
import atexit
from lxml import etree
from subprocess import call
import tarfile

# import the ciop functions (e.g. copy, log)
sys.path.append('/opt/anaconda/bin/')
import cioppy
ciop = cioppy.Cioppy()
 
## register all drivers
#gdal.AllRegister()
## get the Imagine driver and register it
#driver = gdal.GetDriverByName('HFA')
#driver.Register()




# define the exit codes
SUCCESS = 0
ERR_BEAM = 2
ERR_NOEXPR = 3
ERR_NOINPUT=4

# add a trap to exit gracefully
def clean_exit(exit_code):
    log_level = 'INFO'
    if exit_code != SUCCESS:
        log_level = 'ERROR'  
   
    msg = {SUCCESS: 'Processing successfully concluded',
           ERR_BEAM: 'Beam_expr failed to process product',
           ERR_NOEXPR: 'No expression provided',
           ERR_NOINPUT: 'No input provided'}
 
    ciop.log(log_level, msg[exit_code])  






##Input declaration
#targetTaxonomy = 'LCCS'         # define the taxonomy of the target classes
##[num,txt,raw] = xlsread('targets.xls','LCCS_targets');     # list with target LCCS classes and respective indicators
#country = "Unknown"
#focalTargets = []
#if targetTaxonomy == "LCCS":
#    if country == "Italy":
#        focalTargets = [
#        ['A12_A4.A11.D1.E1.B10','PLAND'],
#        ['A11_A1.B1.C1.D1.W7.A8.A9.B3','PLAND'],
#        ['A12_A5.A11.B4.E5.A13.B13.E7','PD','SHAPE'],
#        ['A12_A6.A11.B4.XX.E5.A12.B12.E6','PD','SHAPE'],
#        ['A12_A6.A10.B4.XX.E5.A12.B11.E6','PD','SHAPE'],
#        ['A12_A5.A11.B4.E5.A13.B13.E7','PLAND'],
#        ['A12_A6.A11.B4.E5.B12.E6','PLAND'],
#        ['A12_A6.A10.B4.E5.A12.B11.E6','PLAND'],
#        ['A24_A5.A13.B4.C2.E5.B13.E7','PLAND'],
#        ['A24_A6.A12.B4.C2.E5.B11.E6','PLAND'],
#        ['A24_A4.A12.B3.C2.D3.B10','PLAND'],
#        ['A12.A2.A10.B12.E6','PLAND','CA','MESH'],
#        ['A12.A6.A10.F2.F5.F10.G2.B12','PLAND','CA','MESH'],
#        ['A12.A5.A10.B12.E7','PLAND','CA','MESH'],
#        ['A12.A3.A10.D1.E2.B7','PLAND','CA'],
#        ['A12.A4.A10.D1.E2.B9','PLAND','CA'],
#        ['A11.A1.A8.A9.W7','PLAND','CA'],
#        ['A12.A4.A10.D1.E1.B9','PLAND','CA']
#        ]
#    elif country == "Greece":
#        focalTargets = [
#        ['A12.A3.A10.B2.D1.E1.F1','CA','PLAND'],
#        ['A12.A3.A10.B2.D1.E2.F1-B5','CA','PLAND'],
#        ['A12.A3.A10.B2.D1.E2.F1-B7','CA','PLAND'],
#        ['A12.A3.A10.B2.D1.E2-B6','CA','PLAND'],
#        ['A12.A4.A10.B3.D1.E1.F1','CA','PLAND'],
#        ['A12.A4.A11.B3.D1.E2.F1-A12.B9','CA','PLAND'],
#        ['A12.A4.A11.B3-A12.B14','CA','PLAND'],
#        ['A12.A4.A11.B3.C1.F1-A12.B9','CA','PLAND'],
#        ['A12.A5.A14.B4.E5-B13.E6','CA','PLAND'],
#        ['A12.A5.A11.B4.E5-A13.B13.E7','CA','PLAND'],
#        ['A12.A6.A11.B4.C2.E5-A12.B11.E6','CA','PLAND'],
#        ['A24.A4.A12.B3.C2.D3-B10','CA','PLAND'],
#        ['A24.A5.A13.B4.C3.E5.F2.F5.F10.G2-A8.A15.B11.E6.G7','CA','PLAND'],
#        ['A24.A5.A16.B4.C3-A8.A17.B13','CA','PLAND'],
#        ['A24.A6.A12.B4.C3-B11','CA','PLAND'],
#        ['A24.A6.A12.B4.C2.E5-B11.E6','CA','PLAND'],
#        ['B15.A4-A13.A14','CA','PLAND'],
#        ['B15.A4-A13.A16','CA','PLAND'],
#        ['B15.A4-A13.A17','CA','PLAND'],
#        ['B28.A1.B1.C2.D2-A4','CA','PLAND']
#        ]
#    elif country == "Brazil":
#        focalTargets = [
#        ['A12.A3.A10.B2.D1.E1-B5','CA','PLAND'],
#        ['A11.A4.B1.C1.D1.D9','CA','PLAND'],
#        ['A12.A6.A10.B4.F2.F6.F10.G3','CA','PLAND'],
#        ['A11.A4.B6.D1.D9','CA','PLAND'],
#        ['A12.A1.A11.B1.D1.E1.F2.F4.F7.G4','CA','PLAND'],
#        ['B14.A4','CA','PLAND'],
#        ['B27','CA','PLAND'],
#        ['B28','CA','PLAND']
#        ]    
#    elif country == "India":
#        focalTargets = [
#        ['A12.A3.A14.B2.D1.E2.F2.F4.F10.G4-A15.B7.G11','CA','PLAND'],
#        ['A12.A3.A10.B2.D1.E1.F2.F6.F7.G3.F1-B5.E4.F9.G9','CA','PLAND'],
#        ['A11.A2.B1.C2.D3.D9-B4.C3.C7.C17.D6-W7','CA','PLAND']
#        ]
#   
#TARGETS = 'All'
#PSIZE = 2;          # pixel size (in meters)
#CELLSIZE = 1000;    # size of each constructed cell (in meters)
#STEP = 500;         # step that the imaginable sliding window moves to form the next cell (in meters)
#changeTypes = [
#['PLAND','negative'],
#['PD','negative'],
#['MESH','negative'],
#['SHAPE','positive'],
#['CA','negative'],
#['MPS','negative']
#]                       # file with the type of the studied indicator change for each indicator ('negative', 'positive' or 'any')
#CALCINDICATORS = ['PLAND','CA','MESH','PD','SHAPE','MPS']     # the indicators to be calculated and added to the kea file



def findIndex(fClass,focalClass):
    # return the indices of the segments of the selected focal class
    indFocal = list()
    for i in range(len(fClass)):
        if fClass[i] == focalClass:
            indFocal.append(i)

    return indFocal
    


def constructBinaryImage(SegmentLayer,indFocal):
    B = np.zeros(SegmentLayer.shape,dtype=np.int)
    for i in indFocal:
        B[SegmentLayer==i] = 1

    return B
 
 
def calculatePerimeter(PixelList,conCom,value):
    # expand the initial cell by a 0-value pixel in each side
    xSize = conCom.shape[0]
    ySize = conCom.shape[1]
    Cnew = np.zeros((xSize+2,ySize+2),dtype=int)
    Cnew[1:xSize+1,1:ySize+1] = conCom
    # update the pixel coordinates to fit the extended array
    PixelList = PixelList + 1
    # find the perimeter of the patch. For each pixel, add one unit to the
    # perimeter for each side of the pixel that is not adjacent to another
    # pixel of the patch
    perim = 0
    for i in range(PixelList.shape[1]):
        ix = PixelList[0][i]
        iy = PixelList[1][i]
        if Cnew[ix-1][iy]!=value:
            perim += 1
        if Cnew[ix+1][iy]!=value:
            perim += 1
        if Cnew[ix][iy-1]!=value:
            perim += 1
        if Cnew[ix][iy+1]!=value:
            perim += 1
        
    return perim
     
   
def calculatePland(C):
    # area of habitat of interest in the total area (in pixels)
    a = np.sum(C)
    # total area
    A = C.size
    # PLAND
    PLAND = 100*a/float(A);

    return PLAND
    
    
def calculateMesh(C,pSize):
    # define a structuring element for 8-connectivity
    se = pymorph.img2se(np.ones((3,3),dtype=bool))
    # find connected components with 8-connectivity. An array with the same
    # dimensions as C is returned, assigning the same label to connected
    # pixels, ranging from 1 to the number of connected patches, ignoring
    # pixels with 0 value
    conCom = pymorph.label(C,Bc=se)
    # for each patch, calculate its area in meters
    numPatches = np.amax(conCom)  
    a = np.empty((numPatches),dtype=int)
    for i in range(numPatches):
        numPixels = np.sum(conCom==i+1)
        a[i] = numPixels * (pSize**2)
    # areas squared
    a2 = np.square(a)
    # total area in square meters
    A = (C.size) * (pSize**2)
    # MESH
    MESH = np.sum(a2)/float(10000*A)
    
    return MESH


def calculatePd(C,pSize):
    # define a structuring element for 8-connectivity
    se = pymorph.img2se(np.ones((3,3),dtype=bool))
    # find connected components with 8-connectivity. An array with the same
    # dimensions as C is returned, assigning the same label to connected
    # pixels, ranging from 1 to the number of connected patches, ignoring
    # pixels with 0 value
    conCom = pymorph.label(C,Bc=se)
    # number of patches
    numPatches = np.amax(conCom)  
    # total area in square meters
    A = (C.size) * (pSize**2)
    # PD
    PD = 100*10000*numPatches/float(A);

    return PD


def calculateShape(C,pSize):
    # define a structuring element for 8-connectivity
    se = pymorph.img2se(np.ones((3,3),dtype=bool))
    # find connected components with 8-connectivity. An array with the same
    # dimensions as C is returned, assigning the same label to connected
    # pixels, ranging from 1 to the number of connected patches, ignoring
    # pixels with 0 value
    conCom = pymorph.label(C,Bc=se)
    # number of patches
    numPatches = np.amax(conCom)  
    # for each patch, calculate SHAPE
    SHAPE = np.zeros(numPatches,dtype=float)
    for i in range(numPatches):
        # area of the patch in meters
        numPixels = np.sum(conCom==i+1)
        a = numPixels * (pSize**2)
        # find the coordinates of the pixels of the patch (stored in a 
        # 2 x numPixels array)
        PixelList = np.where(conCom==i+1)
        PixelList = np.array(PixelList)
        # calculate the perimeter of the patch in pixels
        ppix = calculatePerimeter(PixelList,conCom,i+1)
        # perimeter in meters
        p = ppix * pSize
        # SHAPE for the patch
        SHAPE[i] = 0.25*p/float(math.sqrt(a))
        
    # mean SHAPE of all patches
    SHAPE_MN = np.mean(SHAPE)
    
    return SHAPE_MN


def calculateCa(C,pSize):
    # area of target class in the total area (in pixels)
    a = np.sum(C)
    # area in square meters
    a = a * (pSize**2)
    # CA (area in hectares)
    CA = a / float(10000)
    
    return CA
    
    
def calculateMps(C,pSize):  
    # area of target class in the total area (in pixels)
    a = np.sum(C)
    # area in square meters
    a = a * (pSize**2)
    # area in hectares
    a = a / float(10000)
    # define a structuring element for 8-connectivity
    se = pymorph.img2se(np.ones((3,3),dtype=bool))
    # find connected components with 8-connectivity. An array with the same
    # dimensions as C is returned, assigning the same label to connected
    # pixels, ranging from 1 to the number of connected patches, ignoring
    # pixels with 0 value
    conCom = pymorph.label(C,Bc=se)
    # number of patches
    numPatches = np.amax(conCom)  
    # MPS
    MPS = a/float(numPatches)
    
    return MPS

    
def gridCalculations(B,pSize,cellSize,step,indName):
    xSize = B.shape[0]
    ySize = B.shape[1]
    I = np.zeros((xSize,ySize),dtype = np.float)    # the array with the indicator values
    inCells = np.zeros((xSize,ySize),dtype = np.int)    # 2D array with the number of cells each pixels appears in
    pCell = int(cellSize/pSize)                     # cell size in pixels
    pStep = int(step/pSize);                        # step in pixels
    
    # find the abscissa and ordinate of the upper left corner for all cells
    IX = range(0,xSize-pCell+1,pStep)
    IY = range(0,ySize-pCell+1,pStep)
    if IX[len(IX)-1]!=xSize-pCell:
        IX.append(xSize-pCell)
    if IY[len(IY)-1]!=ySize-pCell:
        IY.append(ySize-pCell)
    
    # calculate the indicator
    for ix in IX:
        for iy in IY:
            C = B[ix:ix+pCell][iy:iy+pCell]     # define the cell
 
            # calculate the indicator values for the cell
            if indName == 'PLAND':
                indValue = calculatePland(C)
            elif indName == 'MESH':
                indValue = calculateMesh(C,pSize)
            elif indName == 'PD':
                indValue = calculatePd(C,pSize)
            elif indName == 'SHAPE':
                indValue = calculateShape(C,pSize)
            elif indName == 'CA':
                indValue = calculateCa(C,pSize)
            elif indName == 'MPS':
                indValue = calculateMps(C,pSize)
            else:
                print("Unknown indicator " + indName)
            
            # add the indicator value to the active pixels
            I[ix:ix+pCell][iy:iy+pCell] = I[ix:ix+pCell][iy:iy+pCell] + indValue*C;
            #print("Array I:  shape = "+str(I.shape)+",  type: "+str(I.dtype))
            # update the array with the pixel appearances in cells
            inCells[ix:ix+pCell][iy:iy+pCell] = inCells[ix:ix+pCell][iy:iy+pCell] + 1;
            #print("Array inCells:  shape = "+str(inCells.shape)+",  type: "+str(inCells.dtype))

    # for each pixel, average the values it has been assigned, for each
    # indicator
    I = np.divide(I,inCells.astype(float))
    
    return I


def calculatePatchInd(I,SegmentLayer,indFocal,indicatorsPatch):
    # for each patch, create a binary mask, caluate the indicator and 
    # update the respective cell in the column with the indicator values
    # for all patches
    for i in indFocal:
        # create the binary mask
        B = np.zeros(SegmentLayer.shape,dtype=np.float)
        B[SegmentLayer==i] = 1
        # number of pixels of the patch
        numPixels = np.sum(B)
        
        # isolate the indicator values for the pixels of the patch
        B = np.multiply(B,I)
        # find the mean indicator value characterizing the patch
        sumInd = np.sum(B)
        meanInd = sumInd/float(numPixels)

        # update the column with the indicator values
        indicatorsPatch[i] = meanInd
        
    return indicatorsPatch


def rateImpact(DI,SegmentLayer,indFocal,indName,changeTypes,fClass_p1,fClass_p2,indChangeRating):
    # find the type of change for the specific indicator
    typeChange = []
    for change in changeTypes:
        if change[0] == indName:
            typeChange = change[1]
            break
    
    # If changeType is 'negative', only negative changes, indicating
    # reduction from time 1 to 2, are considered. If 'positive', only
    # positive ones. If 'any', both negative and positive changes are
    # considered, thus absolute changes are taken into account.
    if typeChange == 'positive':
        DI[DI<0.] = 0.
    elif typeChange == 'negative':
        DI[DI>0.] = 0.
        DI = -DI
    else:
        DI = abs(DI)

    # rate the degrees of change, as 0, 1, 2, 3 and 4, when change values
    # are 0, (0,0.25], (0.25,0.5], (0.5,0.75] and >0.75, respectively.
    Imp = np.ceil(DI/0.25)
    Imp[Imp>4.] = 4.
    Imp = Imp.astype(int)
    DI = []

    # for each patch, rate the impact and update the column with the
    # indicator change values
    for i in indFocal:
        if fClass_p1[i]==fClass_p2[i]:
            # count the 1, 2, 3 and 4 rated pixels
            countP = np.zeros(4,dtype=int)
            # find the ratings for the pixels of the patch
            pixelRatings = Imp[SegmentLayer==i]
            numPixels = np.size(pixelRatings)
            if numPixels>0:
                for j in range(numPixels):
                    if pixelRatings[j] == 1:
                        countP[0] += 1
                    elif pixelRatings[j] == 2:
                        countP[1] += 1
                    elif pixelRatings[j] == 3:
                        countP[2] += 1
                    elif pixelRatings[j] == 4:
                        countP[3] += 1
                        
                # average degree of impact
                impDegree = round((countP[0] + 2*countP[1] + 3*countP[2] + 4*countP[3])/float(numPixels))
                impDegree = int(impDegree)
                # impact extent, defined as the percentage of pixels impacted by the
                # average impact degree, rated in the scale 0-4
                if impDegree > 0:
                    impExtent = np.ceil((countP[impDegree-1]/float(numPixels))/0.25)
                else:
                    count0 = numPixels - np.sum(countP)      # number of pixels of 0 impact degree
                    impExtent = np.ceil((count0/float(numPixels))/0.25)
                # overall impact for the patch
                impExtent = int(impExtent)
                imp = min(impDegree,impExtent)
                
                # update the indicator change rating column of the kea file
                indChangeRating[i] = imp
            
    return indChangeRating


def impactRating(fClass_p1,fClass_p2,indicatorsAllP1,indicatorsAllP2,indChangeRatings,SegmentLayer,targetTaxonomy,targets,pSize,cellSize,step,changeTypes,calcIndicators):
    for focalClass in targets:
        # find the indices of the segments of the selected focal class
        indFocal1 = findIndex(fClass_p1,focalClass)
        indFocal2 = findIndex(fClass_p2,focalClass)
        
        if (indFocal1) or (indFocal2):
            # construct binary images indicating the pixels that belong
            # to the focal class
            B1 = constructBinaryImage(SegmentLayer,indFocal1);
            B2 = constructBinaryImage(SegmentLayer,indFocal2);
            sum1 = np.sum(B1)
            sum2 = np.sum(B2)
            for i in range(len(calcIndicators)):            # calculate all available indicators
                # calculate the indicators in a per pixel basis
                if sum1>0:
                    I1 = gridCalculations(B1,pSize,cellSize,step,calcIndicators[i]);
                if sum2>0:
                    I2 = gridCalculations(B2,pSize,cellSize,step,calcIndicators[i]);
    
                # calculate the indicators per patch and update the
                # attribute columns of the kea file
                if sum1>0:
                    indicatorsAllP1[i] = calculatePatchInd(I1,SegmentLayer,indFocal1,indicatorsAllP1[i])              
                if sum2>0:
                    indicatorsAllP2[i] = calculatePatchInd(I2,SegmentLayer,indFocal2,indicatorsAllP2[i])              
    
                if sum1>0 and sum2>0:
                    # detect changes
                    DI = np.divide(I2-I1,I1)
                    I1 = []
                    I2 = []
                    # rate changes on a scale 0-4, considering Period 1 as
                    # reference
                    indChangeRatings[i] = rateImpact(DI,SegmentLayer,indFocal1,calcIndicators[i],changeTypes,fClass_p1,fClass_p2,indChangeRatings[i])

    return indicatorsAllP1, indicatorsAllP2, indChangeRatings


def findFocalTarget(classes,fTarget):
    indFocal = []           # the indices of the selected segments
    delimeters = re.split('\.|_|-', fTarget)    # the individual attributes/qualifiers/delimeters of the focal target class
    for i in range(len(classes)):
        flag = 1            # flag indicating whether the two names match
        classDelimeters = re.split('\.|_|-',classes[i])
        if classDelimeters[0]!=delimeters[0]:
            flag = 0
        else:
            for delim in delimeters:
                if delim not in classes[i]:
                    flag = 0
                    break
        if flag==1:
            indFocal.append(i)
            
    return indFocal


def rateOverall(classes,focalTargets,calcIndicators,indChangeRatings,overallRatings):
    # Note: focalTargets contains the names of the focal target classes
    # together with the respective indicators to be taken into account for
    # the reating of their changes
    for fTarget in focalTargets:
        fTargetName = fTarget[0]        # the name of the class
        fTargetInds = fTarget[1:]       # the indicators to be considered
        # find the indices of the segments of the selected focal target
        # class. The classes of the selected segments should contain all
        # attributes/qualifiers/delimeters of the focal target class
        indFocal = findFocalTarget(classes,fTargetName)
        # find the indices of the indicators to be considered
        indIndicators = []
        for fInd in fTargetInds:
            indIndicators.append(findIndex(calcIndicators,fInd))
        # for each segment, calucate the mean value of the change of the
        # selected indicators and update the column of the kea file
        for i in indFocal:
            ratings = []
            for j in indIndicators:
                ratings.append(indChangeRatings[j][i])
            overChange = np.mean(ratings)
            overallRatings[i] = int(np.ceil(overChange))
    
    return overallRatings


def main():
    # allow GDAL to throw Python Exceptions
    gdal.UseExceptions()

    #os.environ['BEAM_HOME'] = os.path.join(ciop.application_dir, '/opt/beam-5.0')
    #os.environ['PATH'] = os.path.join(os.environ['BEAM_HOME'], 'bin:' + os.environ['PATH'])

    # create the output folder to store the output products and export it
    output_path = os.path.join(ciop.tmp_dir, 'output')
    os.makedirs(output_path)


    # Loops over all the inputs
    for inputfile in sys.stdin:
        # report activity in log
        ciop.log('INFO', 'The input file is: ' + inputfile)

        # retrieve the MER_RR__1P product to the local temporary folder TMPDIR
        # provided by the framework (this folder is only used by this process)
        # the ciop.copy function will use one of online resource available in
        # the metadata to copy it to the TMPDIR folder
        # the funtion returns the local path so the variable retrieved
        # contains the local path to the MERIS product
        retrieved = ciop.copy(inputfile, ciop.tmp_dir)
        outputname = os.path.basename(retrieved)

        ciop.log('INFO', 'Retrieved ' + os.path.basename(retrieved))

    # open the classes raster file
    try:
        classesDataset = gdal.Open(os.path.basename(ciop.copy(inputfile[0], ciop.tmp_dir)))
    #except RuntimeError, e:    #python 2.x syntax
    except RuntimeError as e:   #python 3 syntax
        print('Classes file cannot be opened')
        print(e)
        sys.exit(1)
    # open the object raster file
    try:
        objectsDataset = gdal.Open(os.path.basename(ciop.copy(inputfile[1], ciop.tmp_dir)))
    #except RuntimeError, e:    #python 2.x syntax
    except RuntimeError as e:   #python 3 syntax
        print('Objects file cannot be opened')
        print(e)
        sys.exit(1)
    
    # find the pixel resolution
    geoClasses = classesDataset.GetGeoTransform()
    pixelSizeClasses = geoClasses[1]
    geoObjects = objectsDataset.GetGeoTransform()
    pixelSizeObjects = geoObjects[1]
    if pixelSizeClasses == pixelSizeObjects:
        pixelSize = pixelSizeClasses
    else:
        print('Classes and Objects files are not of the same resolution. ',
              'They need to be rescaled to match')
        sys.exit(1)
        
    
    # load the parameters
#    # pixel size (in meters)
#    pixelSize = ciop.getparam('pixelSize')      
    # size of each constructed cell (in meters)
    cellSize = ciop.getparam('cellSize')
    # step that the sliding window moves to form the next cell (in meters)
    step = ciop.getparam('step')

    # log the value, it helps debugging. 
    # the log entry is available in the process stderr 
    ciop.log('DEBUG', 'The pixel size is: ' + pixelSize + ' m')
    ciop.log('DEBUG', 'The cell size used is: ' + cellSize + ' m')
    ciop.log('DEBUG', 'The step used is: ' + step + ' m')
    
    # read the raster data
    try:
        classesBand = classesDataset.GetRasterBand(1)
    #except RuntimeError, e:    #python 2.x syntax
    except RuntimeError as e:   #python 3 syntax
        print('No band data in the classes file')
        print(e)
        sys.exit(1)
    try:
        objectsBand = objectsDataset.GetRasterBand(1)
    #except RuntimeError, e:    #python 2.x syntax
    except RuntimeError as e:   #python 3 syntax
        print('No band data in the objects file')
        print(e)
        sys.exit(1)
    
    
    
    
    


    # compress the ESA BEAM results
    os.chdir(output_path)
    with tarfile.open(os.path.join(output_path, outputname + '.tar.gz'), "w:gz") as tar:
        tar.add(outputname + '.dim')
        tar.add(outputname + '.data')
        tar.close()

    os.chdir(ciop.tmp_dir)
   
    # publish the compressed results
    ciop.log('INFO', 'Publishing ' + outputname + '.tar.gz') 
    ciop.publish(os.path.join(output_path, outputname + '.tar.gz'))        








    # CODE 4: Calculate the CA and SHAPE landscape measures
    # Hint 1: The calculation of the measures will be performed per cell; you may 
    # find it useful to create an auxiliary/intermediate binary matrix for each
    # cell, of equal size to the cell, where a pixel will have value '1' if it
    # belongs to the (habitat) class of interest at the moment, and '0'
    # elsewhere.
    # Hint 2: You should not use the object id matrix for the calculation of
    # SHAPE, since for its calculation we would consider as connected pixels 
    # neighboring pixels of the (habitat) class of interest, even if they 
    # belong in different objects. We will consider 8-connectivity, i.e. one 
    # pixel of the same class as another will be considered connected to it if 
    # it is directly i) above, ii) below, iii) left, iv) right, v) above-left,
    # vi) above-right, vii) below-right, or viii) below-left it. You may find 
    # very useful to import the 'pymorph' library, or a similar one.




    # CODE 5: Extract the following outputs:
    # i) a geospatial .tif file where each pixel holds the value of measure CA.
    #    The file should be named 'CA_XX_YY.tif, where XX: the CELLSIZE, e.g. 
    #    '1000', YY: the STEP, e.g. '500'.
    # ii) a geospatial .tif file where each pixel holds the value of measure SHAPE.
    #     The file should be named 'SHAPE_XX_YY.tif, where XX: the CELLSIZE, 
    #     e.g. '1000', YY: the STEP, e.g. '500'.
    # iii) a simple .csv file, named 'values.csv', with the landscape measure 
    #      values of each object/segment in the format:
    #      CA_for_Object1, SHAPE_for_Object1, Class_of_Object1
    #      CA_for_Object2, SHAPE_for_Object2, Class_of_Object2
    #      ...
    #      ...
    #      CA_for_ObjectN, SHAPE_for_ObjectN, Class_of_ObjectN
    #
    #      Note: The csv file should ideally end up with 583 lines and three 
    #      comma-separated numbers in each.










        # read the kea file
        ratDataset = gdal.Open(keafileName,gdal.GA_Update)
        
        # read the focal classes of the segments in times 1 and 2
        fClass_p1 = rat.readColumn(ratDataset,"P1_"+targetTaxonomy)
        fClass_p2 = rat.readColumn(ratDataset,"P2_"+targetTaxonomy)
        numSegments = len(fClass_p1)
        
        if TARGETS == 'All':
            # read the target taxonomy columns for both periods P1 and P2 and
            # extract a list with all classes therein 
            Classes = np.append(np.array(fClass_p1),np.array(fClass_p2))
            Classes = np.unique(Classes)            # find the unique entries
            TARGETS = list(Classes)
            Classes = []                           # clear the memory
            
        # Create three 2D empty lists with the indicator values in periods P1
        # and P2 and the ratings of change between the two periods. Try to
        # populate them reading the kea file. If they do not exist, mark the
        # respective indicator values as unknown (NA).
        indicatorsAllP1 = np.empty((len(CALCINDICATORS),numSegments),dtype = np.dtype('a127'))
        indicatorsAllP2 = np.empty((len(CALCINDICATORS),numSegments),dtype = np.dtype('a127'))
        indChangeRatings = np.empty((len(CALCINDICATORS),numSegments),dtype = np.dtype('a127'))
        for i in range(len(CALCINDICATORS)):
            try:
                indicatorsAllP1[i] = rat.readColumn(ratDataset,"P1_"+CALCINDICATORS[i])
                indicatorsAllP2[i] = rat.readColumn(ratDataset,"P2_"+CALCINDICATORS[i])
                indChangeRatings[i] = rat.readColumn(ratDataset,CALCINDICATORS[i] + "_change_rating")
            except:
                indicatorsAllP1[i][...] = 'NA'
                indicatorsAllP2[i][...] = 'NA'
                indChangeRatings[i][...] = 'NA'
                
        # extract the segmentation layer (array of the size of the image, whose
        # each element has the value of the segment the respective pixel 
        # belongs to)
        SegmentLayer = ratDataset.ReadAsArray(xoff=0, yoff=0, xsize=None, ysize=None, buf_obj=None)
        
        # calculate the individual indicator values and changes for each focal class
        print("Calculating indicators...")
        indicatorsAllP1, indicatorsAllP2, indChangeRatings = impactRating(fClass_p1,fClass_p2,indicatorsAllP1,indicatorsAllP2,indChangeRatings,SegmentLayer,targetTaxonomy,TARGETS,PSIZE,CELLSIZE,STEP,changeTypes,CALCINDICATORS)
        
        # write the values of the indicators and their change ratings in the
        # respective columns of the kea file
        # for period 1:
        for i in range(len(CALCINDICATORS)):
            print("Writing column "+"P1_"+CALCINDICATORS[i]+"...")
            rat.writeColumn(ratDataset, "P1_"+CALCINDICATORS[i], indicatorsAllP1[i])
        # for period 2:
        for i in range(len(CALCINDICATORS)):
            print("Writing column "+"P2_"+CALCINDICATORS[i]+"...")
            rat.writeColumn(ratDataset, "P2_"+CALCINDICATORS[i], indicatorsAllP2[i])
        # for change rating from period 1 to period 2:
        for i in range(len(CALCINDICATORS)):
            print("Writing column "+CALCINDICATORS[i] + "_change_rating...")
            rat.writeColumn(ratDataset, CALCINDICATORS[i] + "_change_rating", indChangeRatings[i])
            
        # if specific focal targets and the respective indicators are specified,
        # create a column and place the average value of the selected indicators
        if focalTargets:
            overallRatings = np.empty(numSegments,dtype = np.dtype('a127'))
            overallRatings[...] = 'NA'
            overallRatings = rateOverall(fClass_p1,focalTargets,CALCINDICATORS,indChangeRatings,overallRatings)
            print("Writing column "+"Ind_Combined_Change...")
            rat.writeColumn(ratDataset, "Ind_Combined_Change", indChangeRatings[i])

        print("Calculation of indicators is finished.")






try:
    main()
except SystemExit as e:
    if e.args[0]:
         clean_exit(e.args[0])
    raise
else:
    atexit.register(clean_exit, 0)


