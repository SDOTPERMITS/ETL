import arcpy
from collections import namedtuple, defaultdict, OrderedDict

from impactsFunctions import *

"""
Every record from MVW_GIS_USE
with every record of MVW_GIS_USE_LEGACY (some NULL fields, as LEGACY does not have all the same fields as USE

    For each of these, joined many to one to MVW_GIS_PERMIT

    WIth geometry created using MVW_GIS_BLOCKFACE and street directions


"""


pathSDE     = r'M:\Devapps\HNSPD\DBConnect\gisuser to GISP Direct Connect.sde'
pathHansen8 = r'M:\Devapps\HNSPD\DBConnect\Hansen8 Read to Prod.sde'
pathGDB     = r'V:\StUse\09 - Data and GIS\Data\STREETUSE.gdb'

#COMBINE THE USE and LEGACY USE tables into a single inmeory table
#THIS GUARENTEES THAT ALL RECORDS HAVE THE SCHEMA OF THE MOST RECENT (NULL values)
tblMVWPermitUses            = pathHansen8 + '\\HANSEN_RPT.MVW_GIS_USE'
tblMVWPermitUses_LEGACY     = pathHansen8 + '\\HANSEN_RPT.MVW_GIS_USE_LEGACY'
tblMVWPermitImpacts         = arcpy.CopyRows_management(tblMVWPermitUses, 'in_memory\\USES')[0]
arcpy.Append_management(tblMVWPermitUses_LEGACY, tblMVWPermitImpacts, 'NO_TEST')

sqlUses =(None, 'ORDER BY PERMIT_KEY')

lfMVWPermitImpacts      = '*'
cursorMVWPermitImpacts  = arcpy.da.SearchCursor(tblMVWPermitImpacts, lfMVWPermitImpacts, sql_clause = sqlUses )
ntMVWPermitImpacts      = namedtuple('ntMVWPermitImpacts', cursorMVWPermitImpacts.fields)

print 'loaded uses'



#PUT RELEVENT SDOT STREETS INFORMATION INTO A DICT KEYED BY COMPKEY
fcStreets = pathSDE + '\\SDOT.Streets'
lfStreets = ['COMPKEY', 'SEGDIR', 'DIRLO', 'DIRHI', 'ONSTREET']
ntStreets = namedtuple('ntStreets', lfStreets)
wcStreets = ''
cursorStreets = arcpy.da.SearchCursor(fcStreets, lfStreets, wcStreets)
dictStreets = {}
for rowStreet in cursorStreets:
    dictStreets[rowStreet[0]] = ntStreets(*rowStreet)
del cursorStreets


print 'loaded streets (should use block prolly'


#PUT BLOCKFACES IN A 2-DEEP DICT KEYED BY SEGKEY AND SIDE
tblMVWBlockfaces = pathHansen8 +'\\HANSEN_RPT.MVW_GIS_BLOCKFACE'
lfBlockface = ['SEGKEY', 'DISTANCE', 'END_DISTANCE', 'WIDTH', 'ELMNTKEY']
wcBlockface = ''
cursorBlockface = arcpy.da.SearchCursor(tblMVWBlockfaces, lfBlockface, wcBlockface)
ntBlockface = namedtuple('ntBlockface', lfBlockface)
dictBlockface = defaultdict(dict)
dictBlockface ["SEGKEY"]= {
                            -1/abs(-1): 'blockfaceLeft',
                           0:           'block',
                           1/abs(1):    'blockfaceRight' }

for rowBlockface in cursorBlockface:
    ntupBlockface = ntBlockface(*rowBlockface)
    side = getSideFromWidth(ntupBlockface.WIDTH)
    dictBlockface[ntupBlockface.SEGKEY][side] = ntupBlockface
del cursorBlockface

print 'loaded blockfaces'

#LOAD UP PERMIT LEVEL INFORMATION INTO A DICT KEYED BY PERMIT NUMBER
tblMVWPermit            = pathHansen8 + '\\HANSEN_RPT.MVW_GIS_PERMIT'
tblMVWPermit            = arcpy.CopyRows_management(tblMVWPermit, r'in_memory/permit')[0]
lfMVWPermit             = '*'
sqlPermit =('DISTINCT PERMIT_KEY', 'ORDER BY PERMIT_KEY')#ENFORCE ONE RECORD PER PERMIT
cursorMVWPermit         = arcpy.da.SearchCursor(tblMVWPermit, lfMVWPermit, sql_clause = sqlPermit)
ntMVWPermit             = namedtuple('ntMVWPermit', cursorMVWPermit.fields)


dictNTupPermit = {}
for rowMVWPermit in  cursorMVWPermit:
    ntupPermit = ntMVWPermit(*rowMVWPermit)
    dictNTupPermit[ntupPermit.PERMIT_KEY] = ntupPermit


print 'loaded permit'

#TARGET 
fcTargetImpacts = pathGDB + '\\SU_Permit_Impacts'
tblImpactEvents = arcpy.CreateTable_management('in_memory', 'tblImpactEvents', fcTargetImpacts)
lfImpactEvents = map(lambda f: f.name, filter(lambda f: not f.required, arcpy.ListFields(tblImpactEvents)))
ntLinearRef = namedtuple('LR', ['SEGKEY', 'DISTANCE', 'END_DISTANCE', 'WIDTH', 'COMPKEY'])
dictImpactEventSchema = OrderedDict(map(lambda f: (f, None), lfImpactEvents))

print 'loaded impacts (target'

#===============
#ntupPermit = ntMVWPermit(*cursorMVWPermit.next()) #SORTING FAILS

setAPKEYNotFound = set()
#BUILD A TABLE WITH START_DISTACE, END_DISTANCE AND OFFSET FROM THE BLOCKFACE RECORDS, modified by the closuretype
with arcpy.da.InsertCursor(tblImpactEvents, lfImpactEvents) as insertCurTblImpactLocations:
    
    for rowMVWPermitImpact in cursorMVWPermitImpacts:
         
        impact = ntMVWPermitImpacts(*rowMVWPermitImpact)
        try:

            ntupPermit = dictNTupPermit[impact.PERMIT_KEY]
        except KeyError:
            setAPKEYNotFound.add(impact.PERMIT_KEY)
        """
        if impact.PERMIT_KEY < ntupPermit.PERMIT_KEY:
            ntupPermit = dictNTupPermit[impact.PERMIT_KEY]
            #ntupPermit = ntMVWPermit(*cursorMVWPermit.next())
        """
        
        segkey = impact.SEGKEY
        loctype = impact.LOC_TYPE        

        if impact.SIDE_OF_STREET == 'FC':            
            if impact.LOC_TYPE == 'STREET':
                #use only the centerline for full street closures
                lrInfo = getLRInfoFromBLOCKFACE(segkey, loctype, 0, dictBlockface, ntLinearRef)#CREATE A NEW ROW
                newRow = fieldMapNewRow(ntupPermit, impact, lrInfo,  dictImpactEventSchema)
                insertCurTblImpactLocations.insertRow(newRow)
            else:
                # create two records, assuming both assets on either side are impacted
                for side in [1, -1]:                    
                    lrInfo = getLRInfoFromBLOCKFACE(segkey, loctype, side, dictBlockface, ntLinearRef)#CREATE A NEW ROW
                    newRow = fieldMapNewRow(ntupPermit, impact, lrInfo, dictImpactEventSchema)
                    insertCurTblImpactLocations.insertRow(newRow)     
        else:
            try:
               street = dictStreets[impact.SEGKEY]
            except KeyError:
                #IMPACT SEGKEY DOES NOT EXIST
                pass
            else:
               streetDir = street.DIRHI
               if streetDir is None or streetDir == ' ':
                   if street.ONSTREET and len(street.ONSTREET) > 3:
                       # MAKE AN INFORMED GUESS ABOUT THE DIRECTION OF THE STREET
                       if street.ONSTREET [-2:] == 'ST':
                           streetDir = 'N'
                       elif street.ONSTREET [-3:] == 'AVE':
                           streetDir = 'W'
                       else:
                           streetDir = 'NW'
                   else:
                        streetDir = 'NW'
               impactSide = getSide(streetDir, impact.SIDE_OF_STREET)

               lrInfo = getLRInfoFromBLOCKFACE(segkey, loctype, impactSide, dictBlockface, ntLinearRef) #CREATE A NEW ROW
               newRow = fieldMapNewRow(ntupPermit, impact, lrInfo, dictImpactEventSchema)
               if impact.PERMIT_NO_NUM == '354368':
                   foo = ungraceful
               #insertCurTblImpactLocations.insertRow(newRow)
           

#====================
# ADD ALL THE NEW RECORDS TO A TABLE.

#LINEAR REFERENCE THE TABLE
flyrImpacts = arcpy.MakeRouteEventLayer_lr (fcStreets, 'COMPKEY', tblImpactEvents, "SEGKEY LINE DISTANCE END_DISTANCE", 'impactsLR', 'WIDTH')[0]

arcpy.TruncateTable_management(fcTargetImpacts)
arcpy.Append_management(flyrImpacts, fcTargetImpacts)


#FOR NOW (7/5/2017, we will just Truncate-Append in all our data.
#TODO - make this update only the records with mod dates greater than the last update date
"""
for row in update cursor (target feature class):
    update 
"""
print 'HOORAY'
    

    
    
