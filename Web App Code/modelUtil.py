"""
    Model related utils
"""
import streamlit as st
import pandas as pd
import math
import queryUtil
import dataAccess
import dateUtil
import datetime

# evaluation related
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score

# fbprophet related
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric, add_changepoints_to_plot, plot_plotly
import json
from prophet.serialize import model_to_json, model_from_json

#@st.cache_data
def createDatasetForEvaluation(Crime_data_2003_to_2004, timeType, selectingCondition):
    # Apply data selecting to Crime_data_2003_to_2004
    selectAll = True if selectingCondition == "" or selectingCondition == False else False
    
    if selectAll:
        theRestDf = Crime_data_2003_to_2004[[True]*len(Crime_data_2003_to_2004)]
    else:
        theRestDf = Crime_data_2003_to_2004.query(selectingCondition)
    theDataset_2003_to_2004 = theRestDf.groupby(theRestDf['Date'].dt.to_period(timeType)).count()['Block']
    theDataset_2003_to_2004 = pd.DataFrame(theDataset_2003_to_2004).reset_index().rename(columns={"Date": "ds", "Block": "y"})
    theDataset_2003_to_2004['ds'] = pd.to_datetime(theDataset_2003_to_2004['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    
    # Check if enough data
    restDataExist = True
    if int(theDataset_2003_to_2004.count()['ds']) < 2: restDataExist = False
    
    return theDataset_2003_to_2004, restDataExist

    # timeType can be H, D, W, M, Y
    # There'll be no model if there's less than 2 data.
    # First False for model, third False for no evaluation
#@st.cache_data
def createProphetModel(neededDf, timeType, selectingCondition):
    #selectingCondition = (neededDf['Primary Type'] == 'BURGLARY') & (neededDf['Location Description'] == 'STREET')
    selectAll = True if selectingCondition == "" or selectingCondition == False else False
    
    # Apply data selecting to neededDf
    if selectAll:
        theDf = neededDf[[True]*len(neededDf)]
    else:
        theDf = neededDf.query(selectingCondition)
    theDataset = theDf.groupby(theDf['Date'].dt.to_period(timeType)).count()['Block']
    theDataset = pd.DataFrame(theDataset).reset_index().rename(columns={"Date": "ds", "Block": "y"})
    theDataset['ds'] = pd.to_datetime(theDataset['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    
    
    
    # Check if there not enough data
    ModelExist = True
    if int(theDataset.count()['ds']) < 2: ModelExist = False
    
    
    # Added Location info to theDataset
    # LocationDiscriptionName = list(theDf['Location Description'].drop_duplicates())
    # LocationDiscription_crosstab = pd.crosstab(theDf['Date'].dt.to_period(timeType), theDf['Location Description']).reset_index().rename(columns={"Date": "ds"})
    # LocationDiscription_crosstab['ds'] = pd.to_datetime(LocationDiscription_crosstab['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    # theDataset = pd.merge(theDataset, LocationDiscription_crosstab, how='outer', on='ds').replace(np.nan, 0)
    
    if ModelExist:
        # Config Prophet
        prophet = Prophet(
            growth='linear',
            seasonality_mode = 'additive'
        )
        if timeType.upper() == 'H':
            prophet.daily_seasonality = True
            prophet.weekly_seasonality = True
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            prophet.yearly_seasonality = True
        if timeType.upper() == 'D':
            prophet.daily_seasonality = True
            prophet.weekly_seasonality = True
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            prophet.yearly_seasonality = True
        if timeType.upper() == 'M':
            prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            prophet.yearly_seasonality = True
        if timeType.upper() == 'Y':
            prophet.yearly_seasonality = True   
        prophet.add_country_holidays(country_name='US')
        # for i in LocationDiscriptionName:
        #     prophet.add_regressor(i)
        
        # Run it
        prophet.fit(theDataset)
    else:
        prophet = False
        
    # First False for model, second False for no evaluation
    return prophet

#@st.cache_data
def generateModelName(timeType, crimeType, locationType, locationValue):
    # timeType can be H, D, W, M, Y
    # crimeType can be ALL, BURGLARY, MOTOR VEHICLE THEFT, THEFT
    # LocationType can be All, Community Area, District, Street, Block, Ward
    FileName = ''
    
    # deal with timeType
    if timeType == 'H':
        FileName += 'ByHour'
    elif timeType == 'D':
        FileName += 'ByDay'
    elif timeType == 'W':
        FileName += 'ByWeek'
    elif timeType == 'M':
        FileName += 'ByMonth'
    elif timeType == 'Y':
        FileName += 'ByYear'
    else:
        return False
    
    # deal with crimeType
    if crimeType == 'ALL':
        FileName += "AllCrime"
    elif crimeType == 'BURGLARY':
        FileName += 'Burglary'
    elif crimeType == 'MOTOR VEHICLE THEFT':
        FileName += 'MotorVehicleTheft'
    elif crimeType == 'THEFT':
        FileName += 'Theft'
    else:
        return False
    
    # deal with Location
    if locationType == 'All':
        FileName += 'WholeCity'
    elif locationType == 'Community Area':
        FileName += 'ByCommunityArea' + locationValue
    elif locationType == 'District':
        FileName += 'ByDistrict' + locationValue
    elif locationType == 'Street':
        FileName += 'ByStreet' + locationValue
    elif locationType == 'Block':
        FileName += 'ByBlock' + locationValue
    elif locationType == 'Ward':
        FileName += 'ByWard' + locationValue
    else:
        return False
    
    return FileName        

#@st.cache_data
def generateModelSelection(crimeType, locationType, locationValue):
# Based on crimeType and locationType
# Get selectingCondition and selectAll value
# double False stands for error
    # crimeSelection = "(neededDf['Primary Type'] == "
    crimeSelection = "`Primary Type` == "
    # #locationSelection = "(neededDf['Location Description'] == "
    # locationSelection = "(neededDf["
    locationSelection = ""
    
    # deal with crimeType
    if crimeType == 'ALL':
        crimeSelection = ""
    elif crimeType == 'BURGLARY':
        crimeSelection += "'BURGLARY'"
    elif crimeType == 'MOTOR VEHICLE THEFT':
        crimeSelection += "'MOTOR VEHICLE THEFT'"
    elif crimeType == 'THEFT':
        crimeSelection += "'THEFT'"
    else:
        return False, False
    
    # deal with Location
    if locationType == 'All':
        locationSelection = ""
    elif locationType == 'Community Area':
        locationSelection += "`Community Area` =="
    elif locationType == 'District':
        locationSelection += "`District` =="
    elif locationType == 'Street':
        locationSelection += "`Street` =="
    elif locationType == 'Block':
        locationSelection += "`Block` =="
    elif locationType == 'Ward':
        locationSelection += "`Ward` =="
    else:
        return False, False
    
    if locationType == 'Street' or locationType == 'Block':
        locationSelection += "'" + locationValue + "'"
    elif locationType == 'Community Area' or locationType == 'District' or locationType == 'Ward':
        locationSelection += locationValue
    
    if not (crimeSelection or locationSelection):
        return None, True
    elif crimeSelection and locationSelection:
        return crimeSelection + " & " + locationSelection, False
    else:
        return crimeSelection + locationSelection, False
    

def saveProphetModel(ModelPath, model, modelName):
    #FileName = generateModelName(timeType, crimeType, locationType)
    FileName = modelName + '.json'
    if not FileName or not model:
        return False
    with open(ModelPath + FileName, 'w') as fout:
        json.dump(model_to_json(model), fout)  # Save model
        return True
    return False
    
#@st.cache_data
def evaluateModel(model, restDataframe):
    y_true = restDataframe
    y_predicted = pd.DataFrame(restDataframe['ds'])
    y_predicted = model.predict(y_predicted)
    
    y_true = y_true['y'].values
    y_predicted = y_predicted['yhat'].values
    
    string1 = ('MAE: %.3f' % mean_absolute_error(y_true, y_predicted))
    string2 = ('MSE: %.3f' % mean_squared_error(y_true, y_predicted))
    string3 = ('RMSE: %.3f' % math.sqrt(mean_squared_error(y_true, y_predicted)))
    string4 = ('Explained variance: %.3f' % explained_variance_score(y_true, y_predicted))
    string5 = ('Coefficient of determination: %.3f' % r2_score(y_true, y_predicted))
    
    string = string1 + "  \n  " + string2 + "  \n  " + string3 + "  \n  " + string4 + "  \n  " + string5
    
    return string
    

def evaluateModelAndSave(model, restDataframe, readmeFile, model_name):
    y_true = restDataframe
    y_predicted = pd.DataFrame(restDataframe['ds'])
    y_predicted = model.predict(y_predicted)
    
    y_true = y_true['y'].values
    y_predicted = y_predicted['yhat'].values
    
    # print('MAE: %.3f' % mean_absolute_error(y_true, y_predicted))
    # print('MSE: %.3f' % mean_squared_error(y_true, y_predicted))
    # print('RMSE: %.3f' % math.sqrt(mean_squared_error(y_true, y_predicted)))
    # print('Explained variance: %.3f' % explained_variance_score(y_true, y_predicted))
    # print('Coefficient of determination: %.3f' % r2_score(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "MAE", mean_absolute_error(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "MSE", mean_squared_error(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "RMSE", math.sqrt(mean_squared_error(y_true, y_predicted)))
    readmeFile.writeEvaluation(model_name, "Explained variance", explained_variance_score(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "Coefficient of determination", r2_score(y_true, y_predicted))

def modelErrorDetect(Reason, timeType, crimeType, locationType):
    print(Reason, "timeType:", timeType, "crimeType:", crimeType, "locationType:", locationType)

# This is the method that does the all the process of creating ONE model creation
# if locationType == All, locationValue will be ignored
# def handleTheModel(neededDf, Crime_data_2003_to_2004, ModelPath, readmeFile, timeType, crimeType, locationType, locationValue = ""):
#     # get name
#     model_name = generateModelName(timeType, crimeType, locationType, locationValue)
#     if not model_name:
#         modelErrorDetect("model_name error!", timeType, crimeType, locationType)
#         return False
#     readmeFile.write(model_name)
#     print("Creating", model_name, "...", end="")
    
#     # get condition
#     selectingCondition, selectAll = generateModelSelection(crimeType, locationType, locationValue)
#     if not (selectingCondition or selectAll):
#         modelErrorDetect("Selecting Condition error!", timeType, crimeType, locationType)
#         return False
    
#     # Create model
#     theModel, restDataframe, restDataframeMatter = createProphetModel(neededDf, timeType, selectingCondition, Crime_data_2003_to_2004, selectAll)
#     readmeFile.write(model_name, isStartTime=False)
    
#     # Evaluate the model
#     ## If the model does exist
#     if theModel:
#         ## If evaluation does exist
#         if restDataframeMatter:
#             evaluateModel(theModel, restDataframe, readmeFile, model_name)
#         ## If evaluation doesn't exist
#         elif not restDataframeMatter:
#             readmeFile.writeEvaluation(model_name, "Evaluation", False)
#         if not saveProphetModel(ModelPath, theModel, model_name):
#             modelErrorDetect("Save Model error!", timeType, crimeType, locationType)
#             return False
#     elif not theModel:
#         # When the model doesn't exist
#         readmeFile.writeEvaluation(model_name, "Existance", False)

#     print("Done!")
#     return True
    
# # If you want to create a lot of the same location type
# def handleModels(neededDf, Crime_data_2003_to_2004, ModelPath, readmeFile, timeType, crimeType, locationType):
#     locationValues = []
#     if locationType == 'All':
#         return handleTheModel(neededDf, Crime_data_2003_to_2004, ModelPath, readmeFile, timeType, crimeType, locationType)
#     elif locationType == 'Community Area':
#         locationValues = [str(int(i)) for i in list(neededDf['Community Area'].drop_duplicates())]
#     elif locationType == 'District':
#         locationValues = [str(int(i)) for i in list(neededDf['District'].drop_duplicates())]
#     elif locationType == 'Street':
#         locationValues = list(neededDf['Street'].drop_duplicates())
#     elif locationType == 'Block':
#         locationValues = list(neededDf['Block'].drop_duplicates())
#     elif locationType == 'Ward':
#         locationValues = [str(int(i)) for i in list(neededDf['Ward'].drop_duplicates())]
#     else:
#         return False
    
#     for locationValue in locationValues:
#         handleTheModel(neededDf, Crime_data_2003_to_2004, ModelPath, readmeFile, timeType, crimeType, locationType, locationValue=locationValue)
        
#     return True


# This generates a model based on what you get from the prediction page
#@st.cache_data
def getModelToUse(TimePrecision, CrimeTypeArray, LocationType, LocationValueArray):
    query = queryUtil.get_CrimeType_and_Location_query(CrimeTypeArray, LocationType, LocationValueArray)
    theModel = createProphetModel(
        dataAccess.return_dataFrames('Crime_data'),
        dateUtil.TimePrecision_to_timeType_dict[TimePrecision],
        query
    )
    return theModel
    
#@st.cache_data
def getEvaluationModelToUse(TimePrecision, CrimeTypeArray, LocationType, LocationValueArray):
    query = queryUtil.get_CrimeType_and_Location_query(CrimeTypeArray, LocationType, LocationValueArray)
    theDataset_2003_to_2004, restDataExist = createDatasetForEvaluation(
        dataAccess.return_dataFrames('Crime_data_2003_to_2004'),
        dateUtil.TimePrecision_to_timeType_dict[TimePrecision],
        query,
    )
    return theDataset_2003_to_2004, restDataExist


def predictMoment(model, moment):
    future = pd.DataFrame(columns=['ds'])
    future = future.append({'ds': moment}, ignore_index=True)
    user_forecast = model.predict(future)
    result = user_forecast['yhat'][0]
    return result


def predictPeriod(model, startTime, endTime, timePrecision):
    future = pd.DataFrame(columns=['ds'])
    
    # future['ds'] = pd.date_range(
    #     "2000-01-01", 
    #     '2002-01-01', 
    #     freq=dateUtil.TimePrecision_to_timeType_dict[timePrecision]
    # )
    future['ds'] = dateUtil.generateTimeList(startTime, endTime, freq=dateUtil.TimePrecision_to_timeType_dict[timePrecision])

    user_forecast = model.predict(future)
    
    result = user_forecast[['ds', 'yhat']]
    #result = user_forecast['yhat']
    
    return result