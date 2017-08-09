import arcpy
import csv
import re
import urllib
import json

from collections import defaultdict



def geocodeLine(strSingleLineInput):
    # returns dict of ESRIJSON
    url = r'http://citygeoproc/arcgis/rest/services/locators/SND/GeocodeServer/findAddressCandidates'
    query = '?&outFields=*&maxLocations=1&f=json&Single+Line+Input='+ strSingleLineInput
    try:
        d = json.loads(urllib.urlopen(url+query).read())['candidates'][0]
    except IndexError:
        return False
    return d




g = geocodeLine

#populate 4 dictionaries with segment info

tosDict = defaultdict(set)
frmsDict= defaultdict(set)
tofrmDict = defaultdict(set)
rowFromKey = dict()
block = r'M:\Devapps\HNSPD\DBConnect\Hansen8 Read to Prod.sde\HANSEN_RPT.MVW_GIS_BLOCK'
blockCur = arcpy.da.SearchCursor(block, ['ONSTREET', 'NORMALIZED_XSTRLO', 'NORMALIZED_XSTRHI', 'SEGKEY'])
for row in blockCur:
    tosDict[row[0]].add(row[1]) #{ON: TO}
    frmsDict[row[0]].add(row[2]) #{ON: FROM}
    tofrmDict[row[0]].add((row[1],row[2])) #{ON: (TO, FROM)}
    
    rowFromKey[row[3]] = row[:3]#{SEGKEY :(ON, TO, FROM)}

# Populate a dict to get COMPKEY from SND ID
sndToComp = dict()
sndCur = arcpy.da.SearchCursor(r'M:\Devapps\HNSPD\DBConnect\gisuser to GISP Direct Connect.sde\TRANSPO.SNDSEG_PV', ['SND_ID', 'COMPKEY'], where_clause = 'COMPKEY <> 0')
for sndseg in sndCur:
    sndToComp[sndseg[0]] = sndseg[1]


def compkeyFromSingleLineInput(strSingleLineInput):
    #given a geocode line input, return a compky (or compkeys) for an intersection for the segment at that location
    d = geocodeLine(strSingleLineInput)
    if d is False:
        return False
    try:
        sndIDs = [int(d['attributes'][u'User_fld'])]
    except KeyError:
        sndIDs = [int(d['attributes'][u'User_fld1'])] + [int(d['attributes'][u'User_fld2'])]
    
    compkeys = map(lambda sndID: sndToComp[sndID], sndIDs)
    if len(compkeys) == 1:
        return compkeys[0]
    else:
        return compkeys

def rowFromImp(strSingleLineInput, p = True):
    comp = compkeyFromSingleLineInput(strSingleLineInput)
    if not comp:
        return False
    def rowFromImp(c, p):
        row = rowFromKey[c]
        if p:
           print '\t'.join(row)
        else:
            return row
    if isinstance(comp, list):
        # allow for multiple returns
        return map(lambda c: rowFromImp(c, p), comp)
    else:
        return rowFromImp(comp, p)

r = rowFromImp

#geocodeLine('9201 DELRIDGE WAY SW')['attributes'][u'User_fld']
    
badvals = []
ct = 0

def glookup(stringy):
    return lookup(*stringy.split('\t'))

def l(s):
    return glookup(s)


def lookup(on, to, frm):
    try:
        tos = tosDict [on]
        frms = frmsDict[on]
    except KeyError:
        return False
    if "DEAD" in to.upper() or "DEAD" in frm.upper():
        tofrm = tofrmDict[on]
        if (to, frm) in tofrm or (frm, to) in tofrm:
            return True
        else:
            return False
    if to in tos and frm in frms:
        return True
    elif frm in tos and to in frms:
        return True
    return False


eval_counter = 0


def cleanRow(row):
    def cleanVal(v):
        v = v.upper().strip()
        v = re.sub(' +',' ',v)
        v = re.sub('[!@#$.]', '', v)
        if not ' RP' in v and not ' ET ' in v:
            v = re.sub(' AV ', ' AVE ', v)
            # ramps are edge case, where AV is the correct sub
        return v
    row = tuple(map(cleanVal, row))
    return row
    
def eval_check(ret = False, check_csv = r'G:\Daniel Rockhold\PACT Sheets 2017\checkVals.csv'):
    badvals = []
    checkedvals = []
    eval_counter = 0
    with open(check_csv, 'r') as check:
        rd = csv.reader(check)
        for row in  rd:
            row = cleanRow(row)
            eval_counter += 1
            res = lookup(*row)
            if not res:
                row = tuple(list(row) + ['BAD'])
                badvals.append(row)
            checkedvals.append(row)
        print len(badvals)
        print eval_counter
        if ret:
            writeBads(vals = checkedvals)
            #return badvals
            






def writeBads(name = r'G:\Daniel Rockhold\PACT Sheets 2017\badvals.csv', vals = badvals):
    with open(name, 'wb') as filey:
        wr = csv.writer(filey)
        for row in vals:
            wr.writerow(row)

#eval_check(True)
