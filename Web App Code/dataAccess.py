'''
    Functions related to data accessing, such as saving and reading necessary csv files and maps
'''

import streamlit as st
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gc
import math
import random
import time
from datetime import datetime
import util
import readmeUtil

# To load full data files into system memory. 
# To use Crime_data, you need to global Crime_data
# Fuller are used for graph generating, it contains 2001 to 2017, but you should only care about location related info
# 2003_to_2004 are data between 2003 to 2004 for model evaluation, ONE YEAR
Crime_data = None
Crime_data_fuller = None
Crime_data_2003_to_2004 = None

def load_fullData():
    print("\nLoading full file data:")
    global Crime_data
    global Crime_data_fuller
    global Crime_data_2003_to_2004
    
    # This to make sure that data file will be read only once
    if 'DataFilesLoaded' not in st.session_state or st.session_state['DataFilesLoaded'] == False:
        Crime_data = None
        Crime_data_fuller = None
        Crime_data_2003_to_2004 = None
        startTime = time.time()
        
        # Reading and processing data
        ## Getting crime_data
        print("Loading datafiles...", end="")
        Crime_2001_to_2004 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2001_to_2004.csv", error_bad_lines=False)
        Crime_2005_to_2007 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2005_to_2007.csv", error_bad_lines=False)
        Crime_2008_to_2011 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2008_to_2011.csv", error_bad_lines=False)
        Crime_2012_to_2017 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2012_to_2017.csv", error_bad_lines=False)
        print("Done!")
        
        ## Combining crime_data
        print("Combining crime_data...", end="")
        Crime_data = pd.concat([Crime_2001_to_2004, Crime_2005_to_2007, Crime_2008_to_2011, Crime_2012_to_2017])
        del Crime_2001_to_2004
        del Crime_2005_to_2007
        del Crime_2008_to_2011
        del Crime_2012_to_2017
        Crime_data['Block'] = Crime_data['Block'].str.upper()
        Crime_data_fuller = Crime_data.copy()
        Crime_data_2003_to_2004 = Crime_data.copy()
        gc.collect()
        print("Done!")
        
        ## Processing and handling for crime_data (not fuller)
        print("\nProcessing Crime_data(not fuller): ")
        print("Dropping duplicated ones...", end="")
        Crime_data.drop_duplicates(subset=['Case Number'], inplace=True)
        print("Done!")
        print("Deleting unnecessary rows and columns...", end="")
        Crime_data.index = Crime_data['Case Number']    
        Crime_data.drop(Crime_data[ 
                        (Crime_data['Primary Type'] != "THEFT") &
                        (Crime_data['Primary Type'] != "MOTOR VEHICLE THEFT") &
                        (Crime_data['Primary Type'] != 'BURGLARY')
                    ].index, inplace=True, axis=0)
        Crime_data.drop(['IUCR', 'ID', 'Description', 'Arrest', 'Domestic', 'Beat', 'FBI Code', 'Updated On', 'Latitude', 'Longitude', 'Location', 'X Coordinate', 'Y Coordinate'], inplace=True, axis=1)
        print("Done!")
        print("Handling NaN, null, None, 0, etc...", end="")
        Crime_data = Crime_data.replace('nan', np.NaN)
        Crime_data.dropna(inplace=True)
        print("Done!")
        print("Handling formats...", end="")
        Crime_data.Date = pd.to_datetime(Crime_data.Date, format="%m/%d/%Y %I:%M:%S %p")
        print("Done!")
        print("Deleting 2017...", end="")
        theBeginningOf2017 = datetime(2017, 1, 1)
        Crime_data.drop(Crime_data[Crime_data['Date'] >= theBeginningOf2017].index, inplace=True, axis=0)
        print("Done!")
        print("Deleting 2004 and before...", end='')
        theBeginningOf2005 = datetime(2005, 1, 1)
        Crime_data.drop(Crime_data[Crime_data['Date'] < theBeginningOf2005].index, inplace=True, axis=0)
        print("Done!")
        print(Crime_data.info())
        
        ## Processing and handling for crime_data_fuller
        print("\nProcessing Crime_data_fuller: ")
        print("Dropping duplicated ones...", end="")
        Crime_data_fuller.drop_duplicates(subset=['Case Number'], inplace=True)
        print("Done!")
        print("Deleting unnecessary rows and columns...", end="")
        Crime_data_fuller.index = Crime_data_fuller['Case Number']    
        Crime_data_fuller.drop(['ID', 'Date', 'IUCR',
           'Primary Type', 'Description', 'Location Description', 'Arrest',
           'Domestic', 'Beat', 'FBI Code',
           'Year', 'Updated On'], inplace=True, axis=1)
        print("Done!")
        print("Handling NaN, null, None, 0, etc...", end="")
        Crime_data_fuller[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']] = Crime_data_fuller[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']].replace(0, np.NaN)
        Crime_data_fuller = Crime_data_fuller.replace('nan', np.NaN)
        Crime_data_fuller.dropna(inplace=True)
        print("Done!")
        print("Handling formats...", end="")
        Crime_data_fuller.Latitude = Crime_data_fuller.Latitude.astype(float)
        Crime_data_fuller = pd.DataFrame(Crime_data_fuller)
        print("Done!")
        print(Crime_data_fuller.info())
        
        
        ## Processing and handling for Crime_data_2003_to_2004
        print("\nProcessing Crime_data_2003_to_2004: ")
        print("Dropping duplicated ones...", end="")
        Crime_data_2003_to_2004.drop_duplicates(subset=['Case Number'], inplace=True)
        print("Done!")
        print("Deleting unnecessary rows and columns...", end="")
        Crime_data_2003_to_2004.index = Crime_data_2003_to_2004['Case Number']    
        Crime_data_2003_to_2004.drop(Crime_data_2003_to_2004[ 
                        (Crime_data_2003_to_2004['Primary Type'] != "THEFT") &
                        (Crime_data_2003_to_2004['Primary Type'] != "MOTOR VEHICLE THEFT") &
                        (Crime_data_2003_to_2004['Primary Type'] != 'BURGLARY')
                    ].index, inplace=True, axis=0)
        Crime_data_2003_to_2004.drop(['IUCR', 'ID', 'Description', 'Arrest', 'Domestic', 'Beat', 'FBI Code', 'Updated On', 'Latitude', 'Longitude', 'Location', 'X Coordinate', 'Y Coordinate'], inplace=True, axis=1)
        print("Done!")
        print("Handling NaN, null, None, 0, etc...", end="")
        Crime_data_2003_to_2004 = Crime_data_2003_to_2004.replace('nan', np.NaN)
        Crime_data_2003_to_2004.dropna(inplace=True)
        print("Done!")
        print("Handling formats...", end="")
        Crime_data_2003_to_2004.Date = pd.to_datetime(Crime_data_2003_to_2004.Date, format="%m/%d/%Y %I:%M:%S %p")
        print("Done!")
        print("Deleting 2004 and later...", end="")
        theBeginningOf2004 = datetime(2004, 1, 1)
        Crime_data_2003_to_2004.drop(Crime_data_2003_to_2004[Crime_data_2003_to_2004['Date'] >= theBeginningOf2004].index, inplace=True, axis=0)
        print("Done!")
        print("Deleting before 2003...", end='')
        theBeginningOf2003 = datetime(2003, 1, 1)
        Crime_data_2003_to_2004.drop(Crime_data_2003_to_2004[Crime_data_2003_to_2004['Date'] < theBeginningOf2003].index, inplace=True, axis=0)
        print("Done!")
        print(Crime_data_2003_to_2004.info())
        

        gc.collect()
        endTime = time.time()
        print("Loading full file data done! Took: " +  time.strftime("%H:%M:%S", time.gmtime(endTime - startTime)) + "\n", end='')
        st.session_state['DataFilesLoaded'] = True
    else:
        print("Already loaded!\n")
        
# Don't forget to close_data when no longer in use
def close_fullData():
    global Crime_data
    global Crime_data_fuller
    global Crime_data_2003_to_2004
    print("Releasing full data memory usage...", end="")
    if 'DataFilesLoaded' in st.session_state:
        del st.session_state['DataFilesLoaded']
    Crime_data = None
    Crime_data_fuller = None
    Crime_data_2003_to_2004 = None
    gc.collect()
    print("Done!")

## Data File Related
DataPath = "../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/"
DataFileName = [ 
    'Chicago_Crimes_2001_to_2004.csv',
    'Chicago_Crimes_2005_to_2007.csv', 
    'Chicago_Crimes_2008_to_2011.csv', 
    'Chicago_Crimes_2012_to_2017.csv'
]

def check_dataFiles():
    return util.checkFiles(DataPath, DataFileName)
        
## Comoonly used DataFrame Related
DataFramePath = "./DataFrames/"
#You'll need to add .csv when accessing in data
DataFrames = [
    "Crime_data",
    "Crime_data_2003_to_2004",
    "DistrictToCoordinates_max", 
    "DistrictToCoordinates_min", 
    "DistrictToCoordinates_mean",
    "DistrictToCoordinates_closest",
    "DistrictToCoordinates_most",
    "StreetNameToCoordinates_max", 
    "StreetNameToCoordinates_min", 
    "StreetNameToCoordinates_mean",
    "StreetNameToCoordinates_closest",
    "StreetNameToCoordinates_most",
    "BlockNameToCoordinates_max", 
    "BlockNameToCoordinates_min", 
    "BlockNameToCoordinates_mean",
    "BlockNameToCoordinates_closest",
    "BlockNameToCoordinates_most",
    "WardToCoordinates_max", 
    "WardToCoordinates_min", 
    "WardToCoordinates_mean",
    "WardToCoordinates_closest",
    "WardToCoordinates_most",
    "CommunityAreaToCoordinates_max", 
    "CommunityAreaToCoordinates_min", 
    "CommunityAreaToCoordinates_mean",
    "CommunityAreaToCoordinates_closest",
    "CommunityAreaToCoordinates_most"]
def check_dataFrames():
    return util.checkFiles(DataFramePath, DataFrames, fileNameExtension=".csv")

def create_dataFrames():    
    global Crime_data
    
    # Readme file 
    if not os.path.exists(DataFramePath):
        os.makedirs(DataFramePath)
    readmeFile = readmeUtil.ReadmeUtil(DataFramePath)
    readmeFile.write("Creating DataFrames")

    print("\nCreating DataFrames:")
    
    # Getting needed dataframes
    print("Generating dataframes in memory...", end="")
    
    ## District
    DistrictToCoordinates_max, DistrictToCoordinates_min, DistrictToCoordinates_mean, DistrictToCoordinates_closest, DistrictToCoordinates_most = util.create_dataframe_coordinate_max_min_mean_closest_most('District', Crime_data_fuller)
    ## Streets
    newPd = Crime_data_fuller
    newPd['Street'] = pd.DataFrame(generateStreets(newPd))
    StreetNameToCoordinates_max, StreetNameToCoordinates_min, StreetNameToCoordinates_mean, StreetNameToCoordinates_closest, StreetNameToCoordinates_most =  util.create_dataframe_coordinate_max_min_mean_closest_most('Street', newPd)
    ## Block
    BlockNameToCoordinates_max, BlockNameToCoordinates_min, BlockNameToCoordinates_mean, BlockNameToCoordinates_closest, BlockNameToCoordinates_most = util.create_dataframe_coordinate_max_min_mean_closest_most('Block', newPd)
    ## Ward
    WardToCoordinates_max, WardToCoordinates_min, WardToCoordinates_mean, WardToCoordinates_closest, WardToCoordinates_most = util.create_dataframe_coordinate_max_min_mean_closest_most('Ward', newPd)
    ## Community Area
    CommunityAreaToCoordinates_max, CommunityAreaToCoordinates_min, CommunityAreaToCoordinates_mean, CommunityAreaToCoordinates_closest, CommunityAreaToCoordinates_most = util.create_dataframe_coordinate_max_min_mean_closest_most('Community Area', newPd)
    print("Done!")
    readmeFile.write("Creating DataFrames", isStartTime=False)
    
    # Saving needed dataframes
    readmeFile.write("Saving DataFrames")
    print("Saving DataFrames readme file...", end="")
    
    Crime_data.to_csv(DataFramePath + "Crime_data.csv")
    Crime_data_2003_to_2004.to_csv(DataFramePath + "Crime_data_2003_to_2004.csv")
    
    DistrictToCoordinates_max.to_csv(DataFramePath + "DistrictToCoordinates_max.csv")
    DistrictToCoordinates_min.to_csv(DataFramePath + "DistrictToCoordinates_min.csv")
    DistrictToCoordinates_mean.to_csv(DataFramePath + "DistrictToCoordinates_mean.csv")
    DistrictToCoordinates_closest.to_csv(DataFramePath + "DistrictToCoordinates_closest.csv")
    DistrictToCoordinates_most.to_csv(DataFramePath + "DistrictToCoordinates_most.csv")
    
    StreetNameToCoordinates_max.to_csv(DataFramePath + "StreetNameToCoordinates_max.csv")
    StreetNameToCoordinates_min.to_csv(DataFramePath + "StreetNameToCoordinates_min.csv")
    StreetNameToCoordinates_mean.to_csv(DataFramePath + "StreetNameToCoordinates_mean.csv")
    StreetNameToCoordinates_closest.to_csv(DataFramePath + "StreetNameToCoordinates_closest.csv")
    StreetNameToCoordinates_most.to_csv(DataFramePath + "StreetNameToCoordinates_most.csv")
    
    BlockNameToCoordinates_max.to_csv(DataFramePath + "BlockNameToCoordinates_max.csv")
    BlockNameToCoordinates_min.to_csv(DataFramePath + "BlockNameToCoordinates_min.csv")
    BlockNameToCoordinates_mean.to_csv(DataFramePath + "BlockNameToCoordinates_mean.csv")
    BlockNameToCoordinates_closest.to_csv(DataFramePath + "BlockNameToCoordinates_closest.csv")
    BlockNameToCoordinates_most.to_csv(DataFramePath + "BlockNameToCoordinates_most.csv")
    
    WardToCoordinates_max.to_csv(DataFramePath + "WardToCoordinates_max.csv")
    WardToCoordinates_min.to_csv(DataFramePath + "WardToCoordinates_min.csv")
    WardToCoordinates_mean.to_csv(DataFramePath + "WardToCoordinates_mean.csv")
    WardToCoordinates_closest.to_csv(DataFramePath + "WardToCoordinates_closest.csv")
    WardToCoordinates_most.to_csv(DataFramePath + "WardToCoordinates_most.csv")
    
    CommunityAreaToCoordinates_max.to_csv(DataFramePath + "CommunityAreaToCoordinates_max.csv")
    CommunityAreaToCoordinates_min.to_csv(DataFramePath + "CommunityAreaToCoordinates_min.csv")
    CommunityAreaToCoordinates_mean.to_csv(DataFramePath + "CommunityAreaToCoordinates_mean.csv")
    CommunityAreaToCoordinates_closest.to_csv(DataFramePath + "CommunityAreaToCoordinates_closest.csv")
    CommunityAreaToCoordinates_most.to_csv(DataFramePath + "CommunityAreaToCoordinates_most.csv")
    print("Done!")
    
    readmeFile.write("Saving DataFrames", isStartTime=False)
    readmeFile = None
    
    return check_dataFrames()

# To load comonly used dataFrames into the session
def load_dataFrames():
    if 'dataFramesLoaded' in st.session_state and st.session_state['dataFramesLoaded'] == True:
        return True
    elif check_dataFrames() == False:
        return False
    else:
        st.session_state['dataFrames'] = dict()
        for i in DataFrames:
            fileName = DataFramePath +  i + '.csv'
            theFile = pd.read_csv(fileName)
            st.session_state['dataFrames'][i] = theFile
        st.session_state['dataFramesLoaded'] = True
        return True
    
@st.cache_data
def return_dataFrames(dataframeName):
    if check_dataFrames() == False:
        return False
    else:
        fileName = DataFramePath +  dataframeName + '.csv'
        try:
            theFile = pd.read_csv(fileName, parse_dates=['Date'])
            if dataframeName == 'Crime_data' or dataframeName == 'Crime_data_2003_to_2004':
                theFile['Street'] = pd.DataFrame(generateStreets(theFile))
                theFile['Ward'] = theFile['Ward'].astype(int)
                theFile['Community Area'] = theFile['Community Area'].astype(int)
                theFile['District'] = theFile['District'].astype(int)
        except Exception as e:
            theFile = pd.read_csv(fileName)
    return theFile

#@st.cache_data
def generateStreets(Crime_data):
    streetNames = []
    for i in Crime_data['Block']:
        streetName = i.split(' ', 2)
        streetName = streetName[2]
        streetNames.append(streetName)
    #streetNames = list(dict.fromkeys(streetNames))
    return streetNames


#to clear memory used by loaded dataframs
def close_dataFrames():
    util.batch_delele_from_sessionState('dataFrames')
    
## Prepared graphs
PreparedGraphPath = "./PreparedGraphs/"
Graphs = ["District Map", "Ward Map", "Community Area Map"]
def check_preparedGraphs():
    return util.checkFiles(PreparedGraphPath, Graphs, ".png")

# Only time counsuming or full data required graphs will be prepared
def create_preparedGraphs():
    # To Paint the Map it's better to work with all datas
    global Crime_data_fuller
    
    # Creating Folder
    if not os.path.exists(PreparedGraphPath):
        os.makedirs(PreparedGraphPath)
    
    # README file
    print("Generating PreparedGraph readme file...")
    readmeFile = readmeUtil.ReadmeUtil(PreparedGraphPath)
    
    # Paint with District
    util.createAndSaveMap("District", readmeFile, Crime_data_fuller, PreparedGraphPath)
    
    # Paint with Ward
    util.createAndSaveMap("Ward", readmeFile, Crime_data_fuller, PreparedGraphPath)
    
    # Paint with Community Area
    util.createAndSaveMap("Community Area", readmeFile, Crime_data_fuller, PreparedGraphPath)
    
    print("")
    Crime_data_fuller = None
    plt.close('all')   
    #plt.close(fig)
    readmeFile = None
    gc.collect()
    return check_preparedGraphs()

## Prediction Model Related
ModelPath = './Models/'
def check_models():
    return False