# -*- coding: cp1252 -*-
"""for each row in pact sheet
	select all the streets with the ONSTREET of the row
	
	find the street with HI equal to TO Street 
		UNITID2 -> UNITID_HI
	
	FInd the street with LO equal to From Street 
		UNITID2 -> UNITID_LO
 
	SELECT ALL STREETS WHERE THE ((UNITID2<=UNITI_HI) AND (UNITID2 >= UNITIDLO)) OR((UNITID2 >= UNITI_HI) AND (UNITID2 <= UNITIDLO))
	FOR Street in selection, create a new record in the new out table with the street compkey from the selected Segs, the SHAPE and ON from TO From BLOCK"""
import arcpy
from collections import namedtuple, OrderedDict
import os
import csv
import urllib
import json

fieldNames_Maybe = ['Agency / Unit', 'Project Status', 'Project Type', 'Project ID', 'Project Name',
                    'Project Description', 'On Street', 'From ', 'To', 'PM Name', 'PM Phone', 'PM Email',
                    'Communications Contact Name', 'Communications Phone', 'Communications Email', 'Agency Reference',
                    'Funded', 'Construction Start Date', 'Construction End Date', 'Paving C2C and I2I',
                    'Impact Start Date', 'Impact End Date', 'Impact Type', 'Street Use Permit Number']#LOL THESE ARE NOW THE ACTUAL NAMES...

def geoCode(strSingleLineInput, strRetformat='dict'):
    # returns dict of ESRIJSON
    url = r'http://citygeoproc/arcgis/rest/services/locators/SND/GeocodeServer/findAddressCandidates'
    query = '?&outFields=*&maxLocations=1&f=json&Single+Line+Input=' + strSingleLineInput
    try:
        j = json.loads(urllib.urlopen(url + query).read())
        d = j['candidates'][0]
    except:
        return False
    if strRetformat == 'dict':
        return d
    else:
        p = arcpy.Point(d['location']['x'], d['location']['y'])
        if strRetformat == 'point':
            return p
        elif strRetformat == 'geometry':
            sr = j['spatialReference']['wkid']
            pg = arcpy.PointGeometry(p, str(sr))
        return pg
    return False


getValIfInTable = lambda t, f, d=None: getattr(t, f) if hasattr(t, f) else d
getValIfVal = lambda val, d=None, func=lambda v: True: val if func(val) else d

pathGISP = r'M:\Devapps\HNSPD\DBConnect\gisuser to GISP Direct Connect.sde'
pathH8 = r'M:\Devapps\HNSPD\DBConnect\Hansen8 Read to Prod.sde'
pathGDB = r'V:\StUse\09 - Data and GIS\Data\dotMapsSheets.gdb'

fcStreets = pathGISP + '\\' + 'SDOT.Streets'
mvwBlock = pathH8 + '\\' + 'HANSEN_RPT.MVW_GIS_BLOCK'

# tcOut = TupleCollection(fcNewSchema, empty = True, verbose = True)

# LOAD MVW GIS BLOCK INTO A LIST OF NAMED TUPLES
tupBlock = namedtuple('block', ['COMPKEY', 'UNITID', 'UNITID2', 'UNITIDSORT', 'ONSTREET', 'XSTRLO', 'XSTRHI'])
cursorBlock = arcpy.da.SearchCursor(mvwBlock,
                                    field_names=['SEGKEY', 'SEG_UNITID', 'SEG_UNITID2', 'UNITIDSORT', 'ONSTREET', 'ORD_STNAME_CONCAT',
                                                 'NORMALIZED_XSTRLO', 'NORMALIZED_XSTRHI'])
listBlocks = map(lambda row: tupBlock(*row), cursorBlock)  # believe in yourself
del cursorBlock  # DON"T GET CAUGHT STEPPING

# Load streets into a dictionary COMPKEY:SHAPE so we can pilfer some latYs
dictStreet = {'COMPKEY (SEGKEY)': 'SHAPE'}
cursorStreets = arcpy.da.SearchCursor(fcStreets, field_names=['COMPKEY', 'SHAPE@'])
dictStreet = dict((s[0], s[1]) for s in cursorStreets)
del cursorStreets  # DON"T GET CAUGHT TRIPPING

def geoCodeRow(onStreet, loStreet, hiStreet):
    # type: (str, str, str) -> list
    listOnStreets = list(b for b in listBlocks if
                         b.ONSTREET == onStreet)  # TupleCollection(tcStreets, query = lambda tup: tup.ONSTREET = row.onstreet)

    unidHi = next((s.UNITID2 for s in listOnStreets if s.XSTRLO == loStreet),
                  False)  # doesn't really matter which order
    unidLo = next((s.UNITID2 for s in listOnStreets if s.XSTRHI == hiStreet), False)

    if not (unidHi and unidLo):
        return False

    listBlocksBetween = list(b for b in listOnStreets if (
    (b.UNITID2 <= unidHi and b.UNITID2 >= unidLo) or (b.UNITID2 >= unidHi and b.UNITID2 <= unidLo)))
    return listBlocksBetween


# PUT IT ALL IN MEMORIES LIKE STREISAND

def loadSheet(pathSheet, fcOut, fcTemplate=r'V:\StUse\09 - Data and GIS\Data\dotMapsSheets.gdb\dotMapsSchema'):
    fcName = fcOut.rsplit('\\')[-1]
    e = True
    while e:
        try:
            fcTarget = arcpy.CopyFeatures_management(fcTemplate, r'in_memory\\' + fcName)
            e = False
        except arcpy.ExecuteError as e:
            fcName = fcName + '_n'
            # it is not important what the temporary feature class is called.

    S_U_C_C_E_S_S_F_U_L_L_B_O_I_S = 0
    F_A_I_L_B_O_I_S = []
    fields = map(lambda f: f.name, arcpy.ListFields(fcTarget))
    writeCursor = arcpy.da.InsertCursor(fcTarget, ['SHAPE@'] + fields[2:])  # NO OBJECT ID OR SHAPE
    with open(pathSheet, 'r') as fileCSVRead:
        # reader = csv.DictReader(fileCSVRead)
        # for dRow in reader:

        reader = csv.reader(fileCSVRead)
        # LET THEM EAT CAKE
        row = reader.next()
        # THUS SPAKE
        for row in reader:
            row = map(lambda v: None if v == '' else v, row)
            writeRow = OrderedDict.fromkeys(writeCursor.fields)
            writeRow["AGENCY"] = row[0]  # drRow["Agency / Unit"]
            writeRow["STATUS"] = row[1]  # drRow["Project Status"]
            writeRow["TYPE"] = row[2]  # drRow["Project Type"]
            writeRow["ID_PROJECT"] = row[3]  # drRow["Project ID"]
            writeRow["PROJECTNAME"] = row[4]  # drRow["Project Name"]
            writeRow["PROJECTDESC"] = row[5]  # drRow["Project Description"]
            # writeRow["ONSTREET"]       = row[6]  #    drRow["ONSTREET"]
            # writeRow["FROMSTREET"]     = row[7]  #   drRow["From"] EXCISE THE CODE
            # writeRow["TOSTREET"]       = row[8]  #   drRow["To"]
            writeRow["PM_NAME"] = row[9]  # drRow["PM_Name"]
            writeRow["PM_PHONE"] = row[10]  # drRow["PM Phone"]
            writeRow["PM_EMAIL"] = row[11]  # drRow["PM Email"]
            writeRow["CONTACTNAME"] = row[12]  # drRow["Communications Contact Name"]
            writeRow["CONTACTPHONE"] = row[13]  # drRow["Communications Phone"]
            writeRow["CONTACTEMAIL"] = row[14]  # drRow["Communications Email"]
            writeRow["AGENCYREFNO"] = row[15]  # drRow["Agency Reference"]
            writeRow["FUNDED"] = row[16]  # drRow["Funded"]
            writeRow["CONST_START"] = row[17]  # drRow["Construction_Start_Date"]
            writeRow["CONST_END"] = row[18]  # drRow["Construction End Date"]
            writeRow["REPAVEBLOCK"] = row[19]  # drRow["Paving C2C and I2I"]
            writeRow["BUDGETID"] = row[20]  # getValIfInTable(drRow, 'Budget_ID')
            writeRow["IMPACT_START"] = row[21]  # drRow["Impact Start Date"]
            writeRow["IMPACT_END"] = row[22]  # drRow["Impact End Date"]
            writeRow["IMPACTTYPE"] = row[23]  # drRow["Impact Type"]
            writeRow["SU_PERMITNO"] = row[24]  # drRow["Street Use Permit Number"]

            writeRow["ID_PMAC"] = row[25]  # getValIfInTable(drRow, 'PMAC ID')
            writeRow["ID_PLAN"] = row[26]  # getValIfInTable(drRow, 'Plan ID')

            onStreet = row[6]  # drRow["ONSTREET"]
            loStreet = row[7]  # drRow["XSTRLO"]
            hiStreet = row[8]  # drRow["XSTRHI"]

            listBlocksBetween = geoCodeRow(onStreet, loStreet, hiStreet)
            if listBlocksBetween:
                for b in listBlocksBetween:

                    writeRow["ONSTREET"] = b.ONSTREET  # drRow["ONSTREET"]
                    writeRow["FROMSTREET"] = b.XSTRLO  # drRow["XSTRLO"]
                    writeRow["TOSTREET"] = b.XSTRHI  # drRow["XSTRHI"]
                    writeRow["COMPKEY"] = b.COMPKEY
                    try:
                        s = dictStreet[b.COMPKEY]
                        # if this fails , we have bigger problems...
                        writeRow["SHAPE@"] = s  # NOT 'SHAPE', that is a centroid!

                    except:
                        'balls'
                    try:
                        writeCursor.insertRow(writeRow.values())
                    except RuntimeError as e:
                        print writeRow
                        raise e

            else:
                writeRow["ONSTREET"] = onStreet  # drRow["ONSTREET"]
                writeRow["FROMSTREET"] = loStreet  # drRow["XSTRLO"]
                writeRow["TOSTREET"] = hiStreet
                if onStreet:
                    if loStreet:
                        loPoint = geoCode(onStreet + ' & ' + loStreet, 'point')
                        if loPoint:
                            if hiStreet:
                                hiPoint = geoCode(onStreet + ' & ' + hiStreet, 'point')
                            if hiPoint:
                                writeRow["SHAPE@"] = arcpy.Polyline(arcpy.Array([loPoint, hiPoint]))
                            else:
                                writeRow["SHAPE@"] = arcpy.Polyline(loPoint)
                        else:
                            # An address, maybe?
                            addrPoint = geoCode(loStreet + ' ' + onStreet, 'point')
                            if addrPoint:
                                writeRow["SHAPE@"] = arcpy.Polyline(addrPoint)
                            else:
                                writeRow["SHAPE@"] = None  # darn
                                F_A_I_L_B_O_I_S.append(row)
                    else:
                        onPointMaybe = geoCode(onStreet, 'point')
                        if onPointMaybe:
                            writeRow["SHAPE@"] = arcpy.Polyline(onPointMaybe)
                        else:
                            F_A_I_L_B_O_I_S.append(row)

            try:
                writeCursor.insertRow(writeRow.values())
            except RuntimeError as e:
                print writeRow
                raise e
            S_U_C_C_E_S_S_F_U_L_L_B_O_I_S += 1

    print str(S_U_C_C_E_S_S_F_U_L_L_B_O_I_S) + ' total'
    print str(len(F_A_I_L_B_O_I_S)) + 'FAILED'
    if arcpy.Exists(fcOut):
        # arcpy.TruncateTable_management(fcOut)
        arcpy.Append_management(fcTarget, fcOut)
    else:
        arcpy.CopyFeatures_management(fcTarget, fcOut)
    # arcpy.Delete_management(fcTarget)
    return F_A_I_L_B_O_I_S


pathFolder = r'V:\StUse\08-  Project and Construction Coordination\01 -Technology\PACT Replacement\DOTMaps\Data Request\Returned Data Sheets\Ready to Load\For Batch Upload\Ready'

pathGDBOut = r'V:\StUse\09 - Data and GIS\Data\dotMapsSheets.gdb'
fcOut = pathGDBOut + '\\csvLoad'

F_A_I_L_B_O_I_S = []
"""
for root,dirs,files in os.walk(pathFolder):
    for file in files:
        if file.endswith(".csv"):
            pathSheet = pathFolder+'\\'+file
            try:
                print file
                F_A_I_L_B_O_I_S.extend(loadSheet(pathSheet, fcOut))
            except Exception as e:
                
                print e
            print ' '
                
"""

