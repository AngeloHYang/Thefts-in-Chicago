'''
    Utilities related to dataframe queries
'''

import streamlit as st

#@st.cache_data
def createSingleSelection(columnName, toWhat, how="==", toWhatIsStr=True):
    # How can be ==, <=, >=
    #dataframe[columnName] == euqalTo
    string = ""
    
    columnNameSelection = "`" + columnName + "`"
    
    if toWhatIsStr:
        toWhatSelection = "'" + toWhat + "'"
    else:
        toWhatSelection = toWhat
        
    string = "(" + columnNameSelection + " " + how + " " + str(toWhatSelection) + ")"
    return string

#@st.cache_data
def addAnd(string1, string2):
    if string1 == "" or string1 == False or string1 == None:
        return string2
    if string2 == "" or string2 == False or string2 == None:
        return string1
    string = string1 + " & " + string2
    return string

#@st.cache_data
def addOr(string1, string2):
    if string1 == "" or string1 == False or string1 == None:
        return string2
    if string2 == "" or string2 == False or string2 == None:
        return string1
    string = string1 + " or " + string2
    return string

#@st.cache_data
def addNot(string):
    string = "not" + string
    return string

#@st.cache_data
def addParentheses(string):
    string = "(" + string + ")"
    return string

### Below are related to the project
#@st.cache_data
def get_CrimeType_and_Location_query(CrimeTypeArray, LocationType, LocationValueArray):
    arrays = [False, False]
    # Crime Types
    if len(CrimeTypeArray) > 0:
        for i in CrimeTypeArray:
            arrays[0] = addOr(
                arrays[0],
                createSingleSelection('Primary Type', i, toWhatIsStr=True, how="==")
            )
        arrays[0] = addParentheses(arrays[0])
    else:
        arrays[0] = ""
            
    # Location Values
    toWhatIsStr = True
    if LocationType != 'Whole City':
        if LocationType == 'District' or LocationType == 'Ward' or LocationType == 'Community Area' :
            toWhatIsStr = False
        if len(LocationValueArray) > 0:
            for i in LocationValueArray:
                arrays[1] = addOr(
                    arrays[1],
                    createSingleSelection(LocationType, i, toWhatIsStr=toWhatIsStr, how="==")
                )
            arrays[1] = addParentheses(arrays[1])
        else:
            arrays[1] = ''
    else:
        arrays[1] = ''
    
    queryResult = addAnd(arrays[0], arrays[1])
    return queryResult