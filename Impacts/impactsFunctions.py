from collections import namedtuple, defaultdict
import sys

dictReportGroup = {'54B': 'Block Party Playstreets',
'18': 'Cafes',
'18B': 'Cafes',
'51': 'Major Utilities',
'51A': 'Major Utilities',
'UNK': 'None',
'13': 'Public Space Management',
'15': 'Public Space Management',
'3A': 'Public Space Management',
'3B': 'Public Space Management',
'3C': 'Public Space Management',
'52A': 'Public Space Management',
'52D': 'Public Space Management',
'5A': 'Public Space Management',
'12': 'Renewables',
'12A': 'Renewables',
'14': 'Renewables',
'14B': 'Renewables',
'15A': 'Renewables',
'16': 'Renewables',
'16A': 'Renewables',
'16B': 'Renewables',
'17': 'Renewables',
'18A': 'Renewables',
'18C': 'Renewables',
'2': 'Renewables',
'21': 'Renewables',
'21A': 'Renewables',
'21B': 'Renewables',
'27A': 'Renewables',
'29A': 'Renewables',
'2A': 'Renewables',
'3': 'Renewables',
'33': 'Renewables',
'3D': 'Renewables',
'48': 'Renewables',
'5': 'Renewables',
'52': 'Renewables',
'52B': 'Renewables',
'6': 'Renewables',
'6A': 'Renewables',
'7': 'Renewables',
'7A': 'Renewables',
'7B': 'Renewables',
'8': 'Renewables',
'9': 'Renewables',
'45D': 'Reviews',
'45P': 'Reviews',
'1': 'ROW Management',
'22B': 'ROW Management',
'23': 'ROW Management',
'25': 'ROW Management',
'26': 'ROW Management',
'26A': 'ROW Management',
'27': 'ROW Management',
'28': 'ROW Management',
'29': 'ROW Management',
'29B': 'ROW Management',
'29C': 'ROW Management',
'31': 'ROW Management',
'31B': 'ROW Management',
'31C': 'ROW Management',
'31D': 'ROW Management',
'34': 'ROW Management',
'35': 'ROW Management',
'37': 'ROW Management',
'38': 'ROW Management',
'40': 'ROW Management',
'41': 'ROW Management',
'43': 'ROW Management',
'44': 'ROW Management',
'46': 'ROW Management',
'47': 'ROW Management',
'49': 'ROW Management',
'50': 'ROW Management',
'50A': 'ROW Management',
'51B': 'ROW Management',
'51C': 'ROW Management',
'51D': 'ROW Management',
'51E': 'ROW Management',
'51F': 'ROW Management',
'51G': 'ROW Management',
'51H': 'ROW Management',
'51I': 'ROW Management',
'51J': 'ROW Management',
'51K': 'ROW Management',
'51L': 'ROW Management',
'51M': 'ROW Management',
'51N': 'ROW Management',
'51O': 'ROW Management',
'54': 'ROW Management',
'54A': 'ROW Management',
'54C': 'ROW Management',
'55': 'ROW Management',
'55A': 'ROW Management',
'22': 'Shoring & Excavation',
'45': 'SIP',
'45A': 'SIP',
'45B': 'SIP',
'11': 'Street Ends',
'61': 'Term Limited Permits',
'61A': 'Term Limited Permits',
'61B': 'Term Limited Permits',
'61C': 'Term Limited Permits',
'61D': 'Term Limited Permits',
'61E': 'Term Limited Permits',
'61F': 'Term Limited Permits',
'61G': 'Term Limited Permits',
'61H': 'Term Limited Permits',
'61I': 'Term Limited Permits',
'61J': 'Term Limited Permits',
'61K': 'Term Limited Permits',
'61L': 'Term Limited Permits',
'61M': 'Term Limited Permits',
'61N': 'Term Limited Permits',
'61O': 'Term Limited Permits',
'61P': 'Term Limited Permits',
'33A': 'Truck Permits',
'33B': 'Truck Permits',
'1A': 'Urban Forestry',
'1B': 'Urban Forestry',
'1C': 'Urban Forestry',
'1D': 'Urban Forestry',
'38A': 'Urban Forestry',
'52C': 'Urban Forestry',
'14A': 'Vending',
'14C': 'Vending',
'14D': 'Vending',
'14E': 'Vending',
'19A': 'Vending',
'19B': 'Vending',
'19C': 'Vending',
'19D': 'Vending',
'19E': 'Vending',
'19F': 'Vending',
'19G': 'Vending',
'19H': 'Vending',
'19J': 'Vending',
'19I': 'Vending - Curb space',
'WW100': 'Waterways',
'WW150': 'Waterways',
'WW200': 'Waterways',
'WW250': 'Waterways'}

def getSideFromWidth(width):
    #returns 1, -1, or 0 given some perpendicular offset
    if width > 0:
        return 1
    elif width < 0:
        return -1
    else:
        return 0

def getSide(segDir, side):
    """
    given a two ordinal directions
    hi
             0
        315      45
     270            90
        225      135
            180
    if the impact is on the line

    """
    segDir = 45*['N','NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'].index(segDir)
    try:
        side = 45*['N','NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'].index(side)
    except ValueError:
        return 0

    #recalibrate the circle so that the segdirection is at 0 degrees
    side = side - segDir
    if side < 0:
	    side = side+360    
    segDir = 0

    #Evaluate the difference.
    diff = side - segDir
    if diff < 180:
        # the impact is on the right hand, or positive side of the street
        return 1
    elif diff > 180:
	#impact is on the left side, or negative
        return -1
    else:
	#when the side intersects the segment on the circle, we assume centerline.
        #This is likely invalid data
        return 0

#============================================================

#========================================================================
def getLRInfoFromBLOCKFACE(SEGKEY, LOC_TYPE, side, dictBlockface, lrInfoTup):
    #gathers the linear reference information for a record from the available blockface data
    #calculates the offset based on the type of closure
    #returns a named tuple LR Info capsule with the info required to LR the record
    #THIS IS THE GENERAL CASE, IF WE ARE UNABLE TO FIND A BATTER ASSET MATCH FOR THE IMPACT
    try:
        blockface = dictBlockface[SEGKEY][side]
    except KeyError:
        # if there is no proper blockface or other asset, then just use the centerline
        return lrInfoTup(SEGKEY, 0, 1000, 0, -1)
    else:
        distance = blockface.DISTANCE
        enddistance = blockface.END_DISTANCE
        offset = blockface.WIDTH
        elmtkey = blockface.ELMNTKEY

        if LOC_TYPE in ('STREET', 'TRAVEL LN'):
            #two for a full closure
            offset = int(offset/2) # 0, or half the blockface offset
        elif LOC_TYPE == 'ALLEY': #Assuming parallel, offset is falf of the length of the perp block
            offset = side*150
        elif LOC_TYPE == 'PARKING LN':
            offset = side * ((side * offset)-4)
        elif LOC_TYPE == 'SIDEWALK':
            offset = side * ((side * offset)+6)
        elif LOC_TYPE in ('PLNT STRIP', 'UNIMPR ROW', 'FILLER'):
            offset = side * ((side * offset)+2)
        elif LOC_TYPE ==     'BIKE LANE':
            offset = side * ((side * offset) - 2)
        elif LOC_TYPE == 'XXX':
            #These are from the legacy permits
            pass
            
        lrInfo = lrInfoTup(SEGKEY, distance, enddistance, offset, elmtkey)
        return lrInfo

def fieldMapNewRow(ntupPermit, ntupUse, ntupLinearRef, dictImpactEventSchema):
    #FIELDS FROM MVW_GIS_PERMIT=========================================================== 
    dictImpactEventSchema['PERMIT_AP_TYPE']             =       ntupPermit.PERMIT_AP_TYPE
    dictImpactEventSchema['PERMIT_NO_NUM']              =       ntupPermit.PERMIT_NO_NUM
    dictImpactEventSchema['PERMIT_KEY']                 =       ntupPermit.PERMIT_KEY
    dictImpactEventSchema['PERMIT_CATEGORY_TYPE']       =       ntupPermit.PERMIT_CATEGORY_TYPE
    dictImpactEventSchema['PERMIT_APPPLICATION_DATE']   =       ntupPermit.PERMIT_APPPLICATION_DATE
    dictImpactEventSchema['PERMIT_STAGE_NAME']          =       ntupPermit.PERMIT_STAGE_NAME
    dictImpactEventSchema['PERMIT_STAT']                =       ntupPermit.PERMIT_STAT
    dictImpactEventSchema['PERMIT_ADDRESS_TEXT']        =       ntupPermit.PERMIT_ADDRESS_TEXT
    dictImpactEventSchema['ADDRESS_KEY']                =       ntupPermit.ADDRESS_KEY
    dictImpactEventSchema['SEGKEY']                     =       ntupPermit.SEGKEY
    dictImpactEventSchema['PERMIT_INSPTN_DISTRICT_NAME']=       ntupPermit.PERMIT_INSPTN_DISTRICT_NAME
    dictImpactEventSchema['PERMIT_INSPECTOR_NAME']      =       ntupPermit.PERMIT_INSPECTOR_NAME
    dictImpactEventSchema['PERMIT_INSPECTOR_PHONE_NUM'] =       ntupPermit.PERMIT_INSPECTOR_PHONE_NUM
    dictImpactEventSchema['PERMIT_LOCATION_TEXT']       =       ntupPermit.PERMIT_LOCATION_TEXT
    dictImpactEventSchema['APPLICANT_NAME']             =       ntupPermit.APPLICANT_NAME
    dictImpactEventSchema['APPLICANT_COMPANY_NAME']     =       ntupPermit.APPLICANT_COMPANY_NAME
    dictImpactEventSchema['APPLICANT_PHONE_NUM']        =       ntupPermit.APPLICANT_PHONE_NUM
    dictImpactEventSchema['CONTACT_24HOUR_NAME']        =       ntupPermit.CONTACT_24HOUR_NAME
    dictImpactEventSchema['CONTACT_24HOUR_PHONE_NUM']   =       ntupPermit.CONTACT_24HOUR_PHONE_NUM
    dictImpactEventSchema['JOB_NUMBER_TEXT']            =       ntupPermit.JOB_NUMBER_TEXT
    dictImpactEventSchema['REVIEW_DESC']                =       ntupPermit.REVIEW_DESC
    dictImpactEventSchema['REVIEW_ACTION_DATE']         =       ntupPermit.REVIEW_ACTION_DATE
    dictImpactEventSchema['REVIEW_STATUS']              =       ntupPermit.REVIEW_STATUS
    dictImpactEventSchema['REVIEWER_NAME']              =       ntupPermit.REVIEWER_NAME
    dictImpactEventSchema['DPD_REFERENCE_NUM']          =       ntupPermit.DPD_REFERENCE_NUM
    dictImpactEventSchema['RESTORE_BY_CODE']            =       ntupPermit.RESTORE_BY_CODE
    dictImpactEventSchema['PLANNED_PROJECT_TEXT']       =       ntupPermit.PLANNED_PROJECT_TEXT
    dictImpactEventSchema['CONSTRUCTION_WAIVER_TEXT']   =       ntupPermit.CONSTRUCTION_WAIVER_TEXT
    dictImpactEventSchema['IMPACT_DATA_FORMAT']         =       ntupPermit.IMPACT_DATA_FORMAT
    #FIELDS FOR LINEAR REFERENCEING========================================================
    dictImpactEventSchema['DISTANCE']	                =	ntupLinearRef.DISTANCE
    dictImpactEventSchema['END_DISTANCE']	        =	ntupLinearRef.END_DISTANCE
    dictImpactEventSchema['WIDTH']	                =	ntupLinearRef.WIDTH #LOGICimport
    dictImpactEventSchema['WIDTH']	                =	ntupLinearRef.WIDTH #LOGICimport
    #FIELDS PRESENT IN BOTH MVW_GIS_USE AND MVW_GIS_USE_LEGACY====================================
    dictImpactEventSchema['USE_CODE']	                =	ntupUse.USE_CODE
    dictImpactEventSchema['USE_SPACE_CODE']	        =	ntupUse.USE_SPACE_CODE
    dictImpactEventSchema['USE_DESC']	                =	ntupUse.USE_DESC
    dictImpactEventSchema['USE_START_DATE']	        =	ntupUse.USE_START_DATE
    dictImpactEventSchema['USE_EXP_DATE']	        =	ntupUse.USE_EXP_DATE
    dictImpactEventSchema['USE_SQFT_NBR']               =	ntupUse.USE_SQFT_NBR
    dictImpactEventSchema['USE_ROLL30_FLAG']	        =	ntupUse.USE_ROLL30_FLAG
    dictImpactEventSchema['REPORT_GROUP']               =       dictReportGroup[ntupUse.USE_CODE]
    #FIELDS PRESENT IN ONLY MVW_GIS_USE===========================================================
    if ntupPermit.IMPACT_DATA_FORMAT == 'NEW':
        dictImpactEventSchema['STREET_DESCRIPTION']             =   	ntupUse.STREET_DESCRIPTION
        dictImpactEventSchema['SIDE_OF_STREET']	                =	ntupUse.SIDE_OF_STREET
        dictImpactEventSchema['ROW_CODE']	                =	ntupUse.ROW_CODE
        dictImpactEventSchema['LOC_TYPE']	                =	ntupUse.LOC_TYPE
        dictImpactEventSchema['CLOSURE_TYPE']	                =	ntupUse.CLOSURE_TYPE
        dictImpactEventSchema['DAY_OR_TIME_RESTRICTION']	=	ntupUse.DAY_OR_TIME_RESTRICTION
        dictImpactEventSchema['PEAK_OK']	                =	ntupUse.PEAK_OK
        dictImpactEventSchema['TCP_ROLL30_FLAG']	        =	ntupUse.TCP_ROLL30_FLAG
        #dictImpactEventSchema['STREET_ID']	                =	ntupUse.STREET_ID
        #dictImpactEventSchema['SEGMENT_ID']	                =	ntupUse.SEGMENT_ID
        #GET A BLOCKFACE SEGMENT AND DERIVE LR INFORMATION
        
    else:
        #DEFAULT IS ALREADY NONE FOR THE FIELDS

    
        
        pass
    return dictImpactEventSchema.values()


    

    
    
