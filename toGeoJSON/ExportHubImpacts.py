import ESRItoGeoJson
import urllib
import json
#get all the permit numbers in the survey
key='AIzaSyDloPy4bZG17gjJJM3nA4QubA3LGixa5EM'
urlSheet = r'https://sheets.googleapis.com/v4/spreadsheets/1iG5b-uoYC7fXgOm1qWZvUpnJcgNQI-gCDiCmRXP0d6o/values/Form%20Responses%201'
rng = '!h2:h1000'
urlJSON = urlSheet + rng+'?key='+key
print urlJSON

d = json.loads(urllib.urlopen(urlJSON).read())
permitNos = tuple(str(i[0]) for i in d['values'] if i)





where_clause = "CLOSURE_TYPE IN ( 'CLOSED', 'INT CLOSUR', 'PRT CLOSED', 'XXX') AND PERMIT_STAT <> 'Complete' AND PERMIT_NO_NUM IN "+str(permitNos)
pathSource = r'V:\StUse\09 - Data and GIS\Data\STREETUSE.gdb\SU_Permit_Impacts' # remember to refresh
fields = ['PERMIT_NO_NUM', 'USE_CODE', 'LOC_TYPE', 'CLOSURE_TYPE', 'DAY_OR_TIME_RESTRICTION', 'PEAK_OK', 'APPLICANT_COMPANY_NAME', 'PERMIT_LOCATION_TEXT','PLANNED_PROJECT_TEXT','USE_START_DATE', 'USE_EXP_DATE', 'REPORT_GROUP']

outfolder = r'V:\StUse\09 - Data and GIS\Data\repos\geo\JSON'
outName = 'HubConstruction.geojson'

outpath = outfolder + '\\' + outName
ESRItoGeoJson.toGeoJson(pathSource, outpath, fields, where_clause, boolPointOnly = True) 
