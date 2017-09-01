
import sys
from collections import namedtuple, defaultdict

dictReportGroup = {'1': ['ROW Management', 'CNSTRCTN'],
                   '1A': ['Urban Forestry', 'URBNFOR'],
                   '1B': ['Urban Forestry', 'URBNFOR'],
                   '1C': ['Urban Forestry', 'URBNFOR'],
                   '1D': ['Urban Forestry', 'URBNFOR'],
                   '2': ['Renewables', 'ANNUALS'],
                   '2A': ['Renewables', 'ANNUALS'],
                   '3': ['Renewables', 'ANNUALS'],
                   '3A': ['Public Space Management', 'ANNUALS'],
                   '3B': ['Public Space Management', 'ANNUALS'],
                   '3C': ['Public Space Management', 'ANNUALS'],
                   '3D': ['Renewables', 'ANNUALS'],
                   '5': ['Renewables', 'ANNUALS'],
                   '5A': ['Public Space Management', 'ANNUALS'],
                   '6': ['Renewables', 'ANNUALS'],
                   '6A': ['Renewables', 'ANNUALS'],
                   '7': ['Renewables', 'ANNUALS'],
                   '7A': ['Renewables', 'ANNUALS'],
                   '7B': ['Renewables', 'ANNUALS'],
                   '8': ['Renewables', 'ANNUALS'],
                   '9': ['Renewables', 'ANNUALS'],
                   '11': ['Street Ends', 'ANNUALS'],
                   '12': ['Renewables', 'ANNUALS'],
                   '12A': ['Renewables', 'ANNUALS'],
                   '13': ['Public Space Management', 'ANNUALS'],
                   '14': ['Renewables', 'ANNUALS'],
                   '14A': ['Vending', 'ANNUALS'],
                   '14B': ['Renewables', 'ANNUALS'],
                   '14C': ['Vending', 'ANNUALS'],
                   '14D': ['Vending', 'ANNUALS'],
                   '14E': ['Vending', 'ANNUALS'],
                   '15': ['Public Space Management', 'ANNUALS'],
                   '15A': ['Renewables', 'ANNUALS'],
                   '16': ['Renewables', 'ANNUALS'],
                   '16A': ['Renewables', 'ANNUALS'],
                   '16B': ['Renewables', 'ANNUALS'],
                   '17': ['Renewables', 'ANNUALS'],
                   '18': ['Cafes', 'ANNUALS'],
                   '18A': ['Renewables', 'ANNUALS'],
                   '18B': ['Cafes', 'ANNUALS'],
                   '18C': ['Renewables', 'ANNUALS'],
                   '19A': ['Vending', 'ANNUALS'],
                   '19B': ['Vending', 'ANNUALS'],
                   '19C': ['Vending', 'ANNUALS'],
                   '19D': ['Vending', 'ANNUALS'],
                   '19E': ['Vending', 'ANNUALS'],
                   '19F': ['Vending', 'ANNUALS'],
                   '19G': ['Vending', 'ANNUALS'],
                   '19H': ['Vending', 'ANNUALS'],
                   '19I': ['Vending - Curb space', 'ANNUALS'],
                   '19J': ['Vending', 'ANNUALS'],
                   '21': ['Renewables', 'ANNUALS'],
                   '21A': ['Renewables', 'ANNUALS'],
                   '21B': ['Renewables', 'ANNUALS'],
                   '22': ['Shoring & Excavation', 'SHREXC'],
                   '22B': ['ROW Management', 'CNSTRCTN'],
                   '23': ['ROW Management', 'CNSTRCTN'],
                   '25': ['ROW Management', 'CNSTRCTN'],
                   '26': ['ROW Management', 'CNSTRCTN'],
                   '26A': ['ROW Management', 'CNSTRCTN'],
                   '27': ['ROW Management', 'CNSTRCTN'],
                   '27A': ['Renewables', 'ANNUALS'],
                   '28': ['ROW Management', 'CNSTRCTN'],
                   '29': ['ROW Management', 'CNSTRCTN'],
                   '29A': ['Renewables', 'ANNUALS'],
                   '29B': ['ROW Management', 'CNSTRCTN'],
                   '29C': ['ROW Management', 'CNSTRCTN'],
                   '31': ['ROW Management', 'CNSTRCTN'],
                   '31B': ['ROW Management', 'CNSTRCTN'],
                   '31C': ['ROW Management', 'CNSTRCTN'],
                   '31D': ['ROW Management', 'CNSTRCTN'],
                   '33': ['Renewables', 'ANNUALS'],
                   '33A': ['Truck Permits', 'CNSTRCTN'],
                   '33B': ['Truck Permits', 'UTIL'],
                   '34': ['ROW Management', 'CNSTRCTN'],
                   '35': ['ROW Management', 'CNSTRCTN'],
                   '37': ['ROW Management', 'CNSTRCTN'],
                   '38': ['ROW Management', 'CNSTRCTN'],
                   '38A': ['Urban Forestry', 'URBNFOR'],
                   '40': ['ROW Management', 'CNSTRCTN'],
                   '41': ['ROW Management', 'CNSTRCTN'],
                   '43': ['ROW Management', 'CNSTRCTN'],
                   '44': ['ROW Management', 'CNSTRCTN'],
                   '45': ['SIP', 'IMPRV'],
                   '45A': ['SIP', 'IMPRV'],
                   '45B': ['SIP', 'IMPRV'],
                   '45D': ['Reviews', 'IMPRV'],
                   '45P': ['Reviews', 'IMPRV'],
                   '46': ['ROW Management', 'CNSTRCTN'],
                   '47': ['ROW Management', 'CNSTRCTN'],
                   '48': ['Renewables', 'ANNUALS'],
                   '49': ['ROW Management', 'CNSTRCTN'],
                   '50': ['ROW Management', 'CNSTRCTN'],
                   '50A': ['ROW Management', 'CNSTRCTN'],
                   '51': ['Major Utilities', 'UTIL'],
                   '51A': ['Major Utilities', 'UTIL'],
                   '51B': ['ROW Management', 'UTIL'],
                   '51C': ['ROW Management', 'UTIL'],
                   '51D': ['ROW Management', 'UTIL'],
                   '51E': ['ROW Management', 'UTIL'],
                   '51F': ['ROW Management', 'UTIL'],
                   '51G': ['ROW Management', 'UTIL'],
                   '51H': ['ROW Management', 'UTIL'],
                   '51I': ['ROW Management', 'UTIL'],
                   '51J': ['ROW Management', 'UTIL'],
                   '51K': ['ROW Management', 'UTIL'],
                   '51L': ['ROW Management', 'UTIL'],
                   '51M': ['ROW Management', 'UTIL'],
                   '51N': ['ROW Management', 'UTIL'],
                   '51O': ['ROW Management', 'UTIL'],
                   '52': ['Renewables', 'ANNUALS'],
                   '52A': ['Public Space Management', 'ANNUALS'],
                   '52B': ['Renewables', 'ANNUALS'],
                   '52C': ['Urban Forestry', 'URBNFOR'],
                   '52D': ['Public Space Management', 'ANNUALS'],
                   '54': ['ROW Management', 'CNSTRCTN'],
                   '54A': ['ROW Management', 'CNSTRCTN'],
                   '54B': ['Block Party Playstreets', 'ANNUALS'],
                   '54C': ['ROW Management', 'CNSTRCTN'],
                   '55': ['ROW Management', 'CNSTRCTN'],
                   '55A': ['ROW Management', 'CNSTRCTN'],
                   '61': ['Term Limited Permits', 'TERMS'],
                   '61A': ['Term Limited Permits', 'TERMS'],
                   '61B': ['Term Limited Permits', 'TERMS'],
                   '61C': ['Term Limited Permits', 'TERMS'],
                   '61D': ['Term Limited Permits', 'TERMS'],
                   '61E': ['Term Limited Permits', 'TERMS'],
                   '61F': ['Term Limited Permits', 'TERMS'],
                   '61G': ['Term Limited Permits', 'TERMS'],
                   '61H': ['Term Limited Permits', 'TERMS'],
                   '61I': ['Term Limited Permits', 'TERMS'],
                   '61J': ['Term Limited Permits', 'TERMS'],
                   '61K': ['Term Limited Permits', 'TERMS'],
                   '61L': ['Term Limited Permits', 'TERMS'],
                   '61M': ['Term Limited Permits', 'TERMS'],
                   '61N': ['Term Limited Permits', 'TERMS'],
                   '61O': ['Term Limited Permits', 'TERMS'],
                   '61P': ['Term Limited Permits', 'TERMS'],
                   'UNK': ['None', 'NONE'],
                   'WW100': ['Waterways', 'ANNUALS'],
                   'WW150': ['Waterways', 'ANNUALS'],
                   'WW200': ['Waterways', 'ANNUALS'],
                   'WW250': ['Waterways', 'ANNUALS']

                   }


def getSideFromWidth(width):
    # returns 1, -1, or 0 given some perpendicular offset
    if width > 0:
        return 1
    elif width < 0:
        return -1
    else:
        return 0


def getSide(seg_dir, side):
    """
    determines whether an element falls on the right or left side of a block
    seg_dir : the addressable direction of a street segment; low to high address as ordinal
    side: the side of street of an impact relative to the street, as an ordinal

    returns 1 if side is rigt
            -1 if side is left
            0 if side is center or undetermined

             0
        315      45
     270            90
        225      135
            180
    if the impact is on the line
    
    """
    seg_dir = 45 * ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'].index(seg_dir)
    try:
        side = 45 * ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'].index(side)
    except ValueError:
        return 0

    # recalibrate the circle so that the segment direction is at 0 degrees
    side = side - seg_dir
    if side < 0:
        side = side + 360
    seg_dir = 0

    # Evaluate the difference.
    diff = side - seg_dir
    if diff < 180:
        # the impact is on the right hand, or positive side of the street
        return 1
    elif diff > 180:
        # impact is on the left side, or negative
        return -1
    else:
        # when the side intersects the segment on the circle, we assume centerline.
        # This is likely invalid data
        return 0


# ============================================================

# ========================================================================
def getLRInfoFromBLOCKFACE(SEGKEY, LOC_TYPE, side, dictBlockface, lrInfoTup):
    # gathers the linear reference information for a record from the available blockface data
    # calculates the offset based on the type of closure
    # returns a named tuple LR Info capsule with the info required to LR the record
    # THIS IS THE GENERAL CASE, IF WE ARE UNABLE TO FIND A BATTER ASSET MATCH FOR THE IMPACT
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
            # two for a full closure
            offset = int(offset / 2)  # 0, or half the blockface offset
        elif LOC_TYPE == 'ALLEY':  # Assuming parallel, offset is falf of the length of the perp block
            offset = side * 150
        elif LOC_TYPE == 'PARKING LN':
            offset = side * ((side * offset) - 4)
        elif LOC_TYPE == 'SIDEWALK':
            offset = side * ((side * offset) + 6)
        elif LOC_TYPE in ('PLNT STRIP', 'UNIMPR ROW', 'FILLER'):
            offset = side * ((side * offset) + 2)
        elif LOC_TYPE == 'BIKE LANE':
            offset = side * ((side * offset) - 2)
        elif LOC_TYPE == 'XXX':
            # These are from the legacy permits
            pass

        lrInfo = lrInfoTup(SEGKEY, distance, enddistance, offset, elmtkey)
        return lrInfo


def fieldMapNewRow(ntupPermit, ntupUse, ntupLinearRef, dictImpactEventSchema):
    # FIELDS FROM MVW_GIS_PERMIT===========================================================
    dictImpactEventSchema['PERMIT_AP_TYPE'] = ntupPermit.PERMIT_AP_TYPE
    dictImpactEventSchema['PERMIT_NO_NUM'] = ntupPermit.PERMIT_NO_NUM
    dictImpactEventSchema['PERMIT_KEY'] = ntupPermit.PERMIT_KEY
    dictImpactEventSchema['PERMIT_CATEGORY_TYPE'] = ntupPermit.PERMIT_CATEGORY_TYPE
    dictImpactEventSchema['PERMIT_APPPLICATION_DATE'] = ntupPermit.PERMIT_APPPLICATION_DATE
    dictImpactEventSchema['PERMIT_STAGE_NAME'] = ntupPermit.PERMIT_STAGE_NAME
    dictImpactEventSchema['PERMIT_STAT'] = ntupPermit.PERMIT_STAT
    dictImpactEventSchema['PERMIT_ADDRESS_TEXT'] = ntupPermit.PERMIT_ADDRESS_TEXT
    dictImpactEventSchema['ADDRESS_KEY'] = ntupPermit.ADDRESS_KEY

    # SEGKEY handled along with OLD v NEW format distinctions

    dictImpactEventSchema['PERMIT_INSPTN_DISTRICT_NAME'] = ntupPermit.PERMIT_INSPTN_DISTRICT_NAME
    dictImpactEventSchema['PERMIT_INSPECTOR_NAME'] = ntupPermit.PERMIT_INSPECTOR_NAME
    dictImpactEventSchema['PERMIT_INSPECTOR_PHONE_NUM'] = ntupPermit.PERMIT_INSPECTOR_PHONE_NUM
    dictImpactEventSchema['PERMIT_LOCATION_TEXT'] = ntupPermit.PERMIT_LOCATION_TEXT
    dictImpactEventSchema['APPLICANT_NAME'] = ntupPermit.APPLICANT_NAME
    dictImpactEventSchema['APPLICANT_COMPANY_NAME'] = ntupPermit.APPLICANT_COMPANY_NAME
    dictImpactEventSchema['APPLICANT_PHONE_NUM'] = ntupPermit.APPLICANT_PHONE_NUM
    dictImpactEventSchema['CONTACT_24HOUR_NAME'] = ntupPermit.CONTACT_24HOUR_NAME
    dictImpactEventSchema['CONTACT_24HOUR_PHONE_NUM'] = ntupPermit.CONTACT_24HOUR_PHONE_NUM
    dictImpactEventSchema['JOB_NUMBER_TEXT'] = ntupPermit.JOB_NUMBER_TEXT
    dictImpactEventSchema['REVIEW_DESC'] = ntupPermit.REVIEW_DESC
    dictImpactEventSchema['REVIEW_ACTION_DATE'] = ntupPermit.REVIEW_ACTION_DATE
    dictImpactEventSchema['REVIEW_STATUS'] = ntupPermit.REVIEW_STATUS
    dictImpactEventSchema['REVIEWER_NAME'] = ntupPermit.REVIEWER_NAME
    dictImpactEventSchema['DPD_REFERENCE_NUM'] = ntupPermit.DPD_REFERENCE_NUM
    dictImpactEventSchema['RESTORE_BY_CODE'] = ntupPermit.RESTORE_BY_CODE
    dictImpactEventSchema['PLANNED_PROJECT_TEXT'] = ntupPermit.PLANNED_PROJECT_TEXT
    dictImpactEventSchema['CONSTRUCTION_WAIVER_TEXT'] = ntupPermit.CONSTRUCTION_WAIVER_TEXT
    dictImpactEventSchema['IMPACT_DATA_FORMAT'] = ntupPermit.IMPACT_DATA_FORMAT
    # FIELDS FOR LINEAR REFERENCEING========================================================
    dictImpactEventSchema['DISTANCE'] = ntupLinearRef.DISTANCE
    dictImpactEventSchema['END_DISTANCE'] = ntupLinearRef.END_DISTANCE
    dictImpactEventSchema['WIDTH'] = ntupLinearRef.WIDTH  # LOGICimport
    # FIELDS PRESENT IN BOTH MVW_GIS_USE AND MVW_GIS_USE_LEGACY====================================
    dictImpactEventSchema['USE_CODE'] = ntupUse.USE_CODE
    dictImpactEventSchema['USE_SPACE_CODE'] = ntupUse.USE_SPACE_CODE
    dictImpactEventSchema['USE_DESC'] = ntupUse.USE_DESC
    dictImpactEventSchema['USE_START_DATE'] = ntupUse.USE_START_DATE
    dictImpactEventSchema['USE_EXP_DATE'] = ntupUse.USE_EXP_DATE
    dictImpactEventSchema['USE_SQFT_NBR'] = ntupUse.USE_SQFT_NBR
    dictImpactEventSchema['USE_ROLL30_FLAG'] = ntupUse.USE_ROLL30_FLAG

    dictImpactEventSchema['REPORT_GROUP'] = dictReportGroup[ntupUse.USE_CODE][0]
    dictImpactEventSchema['RSPGRPCD'] = dictReportGroup[ntupUse.USE_CODE][1]
    # FIELDS PRESENT IN ONLY MVW_GIS_USE===========================================================
    if ntupPermit.IMPACT_DATA_FORMAT == 'NEW':
        dictImpactEventSchema['STREET_DESCRIPTION'] = ntupUse.STREET_DESCRIPTION
        dictImpactEventSchema['SIDE_OF_STREET'] = ntupUse.SIDE_OF_STREET
        dictImpactEventSchema['ROW_CODE'] = ntupUse.ROW_CODE
        dictImpactEventSchema['LOC_TYPE'] = ntupUse.LOC_TYPE
        dictImpactEventSchema['CLOSURE_TYPE'] = ntupUse.CLOSURE_TYPE
        dictImpactEventSchema['DAY_OR_TIME_RESTRICTION'] = ntupUse.DAY_OR_TIME_RESTRICTION
        dictImpactEventSchema['PEAK_OK'] = ntupUse.PEAK_OK
        dictImpactEventSchema['TCP_ROLL30_FLAG'] = ntupUse.TCP_ROLL30_FLAG
        # dictImpactEventSchema['STREET_ID']	                =	ntupUse.STREET_ID
        # dictImpactEventSchema['SEGMENT_ID']	                =	ntupUse.SEGMENT_ID
        # GET A BLOCKFACE SEGMENT AND DERIVE LR INFORMATION

        dictImpactEventSchema['SEGKEY'] = ntupUse.SEGKEY
    else:
        # DEFAULT IS ALREADY NONE FOR THE FIELDS
        dictImpactEventSchema['SEGKEY'] = ntupPermit.SEGKEY

        pass
    return dictImpactEventSchema.values()
