import arcpy
from collections import OrderedDict

import json

"""
fieldys = [
cursory = arcpy.da.SearchCursor(pathy, 'M')
"""
"""
SADA data is expected to come is as geometry collection. 
     {
         "type": "GeometryCollection",
         "geometries": [{
             "type": "Point",
             "coordinates": [100.0, 0.0]
         }, {
             "type": "LineString",
             "coordinates": [
                 [101.0, 0.0],
                 [102.0, 1.0]
             ]
         }]
     }
"""


#json.dumps(datetime.datetime.now(), default=date_handler)



def getGeo(geometry):
    #implied geometry.isMultiPart is True
        #Maybe make this explicit, holes in polygons are different from multipolygons
    geometryESRIType = geometry.type
    jsonESRIFormat = geometry.JSON.replace(',null', '')#remove the nulls, IDK maybe replace with 'NULL'
            
    if geometryESRIType == u'point':
        geoTypeGEOJSON  = 'Point'
        d =  json.loads(jsonESRIFormat)
        coords = [d['x'], d['y']]
            
        dictGeo = {"geometry" : {
                            "type" : geoTypeGEOJSON,
                            "coordinates": coords # paths not valid for point or multipoint
                            }
                }
    else:
        if geometryESRIType     ==  u'polygon':
            geoTypeGEOJSON  = 'Polygon'
            coordKey = 'rings'
        elif geometryESRIType   == u'multipoint':
            geoTypeGEOJSON  = 'MultiPoint'
            coordKey = 'points'
        elif geometryESRIType   == u'polyline':
            geoTypeGEOJSON  = 'MultiLineString'
            coordKey = 'paths'
          
            
        dictGeo ={  "type" : geoTypeGEOJSON,
                    "coordinates": json.loads(jsonESRIFormat)[coordKey] # paths not valid for point or multipoint
                }
                    
    return dictGeo

def getProperties(dtype, cur, idxsDate=[]):

    date_handler = lambda obj: (
        # thanks https://stackoverflow.com/questions/455580/
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    #additionals = #fudge IT LETS JUST OVERWRITE DATES WITH ISO STRINGS #edit, changed a word
    
    def convertProperty(dt, v):
        for i in range (1, len(cur)): 
            n   = dt[0]
            t   = dt[1]
            if isinstance(v, datetime.datetime):
                v = date_handler(v)
            return (n, v)
        
    return dict(    map(lambda i: convertProperty(dtype[i], cur[i]) , range(1,len(cur)))   )

def genDict(cursor):
    desc = cursor._dtype.descr
    for cur in cursor:
        geometry = cur[0]
        
        dictRow =   OrderedDict((
                           ("type", "Feature"),
                           ("properties", getProperties(desc, cur)), #here is where I would make a iso format for the dates
                           ("geometry", getGeo(cur[0]))
                        ))
        yield dictRow

def toGeoJson(in_table, outPath, field_names = '*', where_clause = '', spatial_reference = '4326', sql_clause =(None, None), explode_to_points = False, allowBlob = False, boolPointOnly = False ):

    shapeType = ("SHAPE@XY" if boolPointOnly else 'SHAPE@')
    

    with open(outPath, 'w') as outfile:
        outfile.write('{"type": "FeatureCollection","features": [\n')
        fields = arcpy.ListFields(in_table)
        
        if field_names == '*':
            pass
        elif type(field_names) in (type(list()), type(tuple())):
           fields = filter(lambda f: f.name in field_names, fields) 
        else:
                raise TypeError(('Not a valid field_names. Use list, tuple or "*"', field_names))
        if not allowBlob:
            #BLOBS are BIG, but maybe okay if we use little pictures. IDK really
            fields = filter(lambda f: f.type <> 'Blob', fields)


        fields = filter(lambda f: 'SHAPE' not in f.name , fields) #NO SHAPES ALLOWED!!1! 
                
        field_names =  [shapeType] +  map(lambda f: f.name, fields)#OKAY, AT THE FRONT IS FINE
        print field_names
        cursor = arcpy.da.SearchCursor(in_table, field_names, where_clause, spatial_reference, explode_to_points, sql_clause)
        
        gen = genDict(cursor)
        json.dump(gen.next(), outfile, indent = 4)
        for d in gen:
            outfile.write(',')
            json.dump(d, outfile, indent = 4)
            
        outfile.write('\n]}')

    
        
pathy = r'M:/Devapps/HNSPD/DBConnect/gisuser to GISP Direct Connect.sde/SDOT.V_SU_PERMITS_IMPACT'
fieldies = ['PERMIT_NO_NUM', 'USE_CODE','USE_EXP_DATE', 'USE_EXP_DATE']
outfolder = r'V:\StUse\09 - Data and GIS\Data\repos\geo\JSON'
outName = '31Ds.geojson'
outpath = outfolder + '\\' + outName
where_clause = 'USE_CODE = "31D"' # GOD FORBID YOU USE THE WRONG KIND OF QUOTES
toGeoJson(pathy,outpath, fieldies, where_clause, boolPointOnly = True)   
