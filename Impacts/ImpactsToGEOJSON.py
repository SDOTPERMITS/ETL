import sys
sys.path.append(r'V:\StUse\09 - Data and GIS\Data\repos\ETL')

from toGeoJSON import *

"""
where_clause = "((PEAK_OK IS NOT NULL AND PEAK_OK <> 'NO') AND CLOSURE_TYPE IN ( 'CLOSED', 'INT CLOSUR', 'PRT CLOSED', 'XXX')  AND LOC_TYPE IN ( 'TRAVEL LN', 'STREET', 'INTRSCTION') AND PERMIT_STAT <> 'Complete')"
pathy = r'V:\StUse\09 - Data and GIS\Data\STREETUSE.gdb\SU_Permit_Impacts' # remember to refresh
fieldies = ['PERMIT_NO_NUM', 'USE_CODE', 'CLOSURE_TYPE', 'DAY_OR_TIME_RESTRICTION', 'PEAK_OK', 'APPLICANT_COMPANY_NAME', 'PERMIT_LOCATION_TEXT','PLANNED_PROJECT_TEXT','USE_EXP_DATE', 'USE_EXP_DATE', 'REPORT_GROUP']
outfolder = r'V:\StUse\09 - Data and GIS\Data\repos\geo\JSON'
outName = 'CurrentConstruction.geojson'
outpath = outfolder + '\\' + outName
toGeoJson(pathy,outpath, fieldies, where_clause, boolPointOnly = True) 
"""
"""
pathy = r'V:\StUse\09 - Data and GIS\Data\STREETUSE.gdb\AccessSeattleGroups'
fields = '*'
outfolder = r'V:\StUse\09 - Data and GIS\Data\repos\geo\JSON'
outName = 'AccessSeattleGroups.geojson'
outpath = outfolder + '\\' + outName
toGeoJson(pathy,outpath, fields)
"""
"""
pathy = r'V:\StUse\09 - Data and GIS\Data\STREETUSE.gdb\AccessSeattleGroups'
fields = '*'
outfolder = r'V:\StUse\09 - Data and GIS\Data\repos\geo\JSON'
outName = 'AccessSeattleGroups.geojson'
outpath = outfolder + '\\' + outName
toGeoJson(pathy,outpath, fields)
"""

"""
#pathy = r'M:/Devapps/HNSPD/DBConnect/gisuser to GISP Direct Connect.sde/SDOT.V_SU_PERMITS_IMPACT' # seems to be failing
pathy = r'V:\StUse\09 - Data and GIS\Data\STREETUSE.gdb\SU_Permit_Impacts' # remember to refresh
fieldies = ['PERMIT_NO_NUM', 'USE_CODE', 'CLOSURE_TYPE', 'DAY_OR_TIME_RESTRICTION', 'PEAK_OK', 'APPLICANT_COMPANY_NAME', 'PERMIT_LOCATION_TEXT','PLANNED_PROJECT_TEXT','USE_EXP_DATE', 'USE_EXP_DATE', 'REPORT_GROUP']
outfolder = r'V:\StUse\09 - Data and GIS\Data\repos\geo\JSON'
outName = 'CurrentConstruction.geojson'
outpath = outfolder + '\\' + outName
where_clause = "PERMIT_NO_NUM = '229683' AND PERMIT_STAT <> 'Complete' AND USE_ROLL30_FLAG = 'Y' AND USE_CODE IN ('51', '51A', '45','45A', '45B')" # " this = 'correct' "
toGeoJson(pathy,outpath, fieldies, where_clause, boolPointOnly = True)   
"""
