from ConfigParser import SafeConfigParser
from . import const
import sys

def getConfig(section, key, dataType=str):
    parser = SafeConfigParser()
    parser.read(const.SETTING_FILE)
    try:
        if dataType == int:
            return parser.getint(section, key)
        elif dataType == float:
            return parser.getfloat(section, key)
        else:
            return parser.get(section, key)
    except Exception as ex:
        sys.exit('Error Reading Configuration: ' + str(ex))