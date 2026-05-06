'''
    Utils about date handling
'''

import streamlit as st
from calendar import monthrange
import datetime

timePrecision = ["Hour", "Day", "Month", "Year"]
TimePrecision_to_timeType_dict = {"Hour": "H", "Day": "D", "Month": "M", "Year": "Y"}
    
@st.cache_data
def getTimePrecisionValue(TimePrecisionName):
    return timePrecision.index(TimePrecisionName)

def generateTimeList(startTime, endTime, freq):
    
    if freq == 'H':
        startTime = datetime.datetime(year=startTime.year, month=startTime.month, day=startTime.day, hour=startTime.hour)
        endTime = datetime.datetime(year=endTime.year, month=endTime.month, day=endTime.day, hour=endTime.hour)
    elif freq == 'D':
        startTime = datetime.datetime(year=startTime.year, month=startTime.month, day=startTime.day)
        endTime = datetime.datetime(year=endTime.year, month=endTime.month, day=endTime.day, hour=endTime.hour)    
    elif freq == 'M':
        startTime = datetime.datetime(year=startTime.year, month=startTime.month, day=1)
        endTime = datetime.datetime(year=endTime.year, month=endTime.month, day=1)
    elif freq == 'Y':
        startTime = datetime.datetime(year=startTime.year, month=1, day=1)
        endTime = datetime.datetime(year=endTime.year, month=1, day=1)
    
    theTime = startTime
    theList = []
    
    while theTime <= endTime:
        theList.append(theTime)
        if freq == 'H':
            theTime += datetime.timedelta(hours=1)
        elif freq == 'D':
            theTime += datetime.timedelta(days=1)
        elif freq == 'M':
            if theTime.month == 12:
                theTime = datetime.datetime(theTime.year + 1, 1, day=1)
            else:
                theTime = datetime.datetime(theTime.year, theTime.month + 1, day=1)
        elif freq == 'Y':
            theTime = datetime.datetime(theTime.year + 1, 1, day=1)
            
    return theList
        
def getFriendlyString(theTime, timePrecision):
    string = ''
    if timePrecision == 'Hour':
        string = theTime.year + "-" + theTime.month + "-" + theTime.day + " " + theTime.hour + ":00"
    elif timePrecision == 'Day':
        string = theTime.year + "-" + theTime.month + "-" + theTime.day
    elif timePrecision == 'Month':
        string = theTime.year + "-" + theTime.month
    elif timePrecision == 'Year':
        string = "the year" + theTime.year
    return string

def customDatePicker(container, labelName, limit='Day'):
    with container:
        howMany = len(timePrecision) - getTimePrecisionValue(limit)
        
        yearNumber = 2000
        monthNumber = 1
        dayNumber = 1
        hourNumber = 0
        
        if howMany >= 1:
            yearNumber = st.number_input(
                label=labelName + ' Year:', 
                min_value=1, 
                max_value=9999,
                step=1,
                value=2000
            )
            
        columns = st.columns(2)
        
        for i in range(1, min(howMany, 3)):
            with columns[i - 1]:
                if i == 1:
                    monthNumber = st.selectbox(
                        label=labelName + ' Month:', 
                        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                    )
                if i == 2:
                    days = [int(j) for j in range(1, monthrange(yearNumber, monthNumber)[1] + 1)]
                    dayNumber = st.selectbox(
                        label=labelName + ' Day:', 
                        options=days
                    )
                    
                    

        if howMany == 4:
            hourNumber = st.number_input(
                label=labelName + ' Hour:', 
                min_value=0, 
                max_value=23,
                step=1,
                value=12
            )
                    
        return datetime.datetime(yearNumber, monthNumber, dayNumber, hourNumber)