"""
    @author: ArcGIS for Water Utilities
    @contact: ArcGISTeamUtilities@esri.com
    @company: Esri
    @version: 1.0.0
    @description: Used to stage the app in your organization.
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
"""

import sys, os, datetime
from arcpy import env
from arcpyhelper import ArcRestHelper
from arcpyhelper import Common

log_file='./logs/PublishDMA.log'

configFiles=['C:/Work/ArcGIS for Utilities/_Water/Staging/A4W-SubDMAProcessor-v1/Application/configs/PublishDMA.json']
globalLoginInfo = 'C:/Work/ArcGIS for Utilities/_Water/Staging/A4W-SubDMAProcessor-v1/Application/configs/GlobalLoginInfo.json'
dateTimeFormat = '%Y-%m-%d %H:%M'

if __name__ == "__main__":
    env.overwriteOutput = True

    log = Common.init_log(log_file=log_file)

    try:

        if log is None:
            print "Log file could not be created"

        print "********************Script Started********************"
        print datetime.datetime.now().strftime(dateTimeFormat)
        webmaps = []
        cred_info = None
        if os.path.isfile(globalLoginInfo):
            loginInfo = Common.init_config_json(config_file=globalLoginInfo)
            if 'Credentials' in loginInfo:
                cred_info = loginInfo['Credentials']
        print "    Logging in"
        arh = ArcRestHelper.publishingtools(username = cred_info['Username'], password=cred_info['Password'],org_url=cred_info['Orgurl'],
                                           token_url=None, 
                                           proxy_url=None, 
                                           proxy_port=None)
        if arh is None:
            print "    Log in not successful"
            
        print "    Logged in successfully"
        
        for configFile in configFiles:

            config = Common.init_config_json(config_file=configFile)
            if config is not None:
                print "  "

                print "  ---------"
                print "    Processing config %s" % configFile
            
                if 'PublishingDetails' in config:
                    if 'FeatureServices' in config['PublishingDetails']:
                        resultFS = arh.publishFsFromMXD(fs_config=config['PublishingDetails']['FeatureServices'])
                    if 'MapDetails' in config['PublishingDetails']:
                    
                        resultMap = arh.publishMap(maps_info=config['PublishingDetails']['MapDetails'],fsInfo=resultFS)
                    #mapInfo =  helper.publish_service_map_from_config(config)
                    #if mapInfo != None:
                        #if 'MapInfo' in mapInfo:
                            #if len(mapInfo['MapInfo']) > 0:
                                #for webmap in mapInfo['MapInfo']:
                                    #if 'ItemID' in webmap:
                                        #webmaps.append(webmap['ItemID'])

                print "    Config %s completed" % configFile
                print "  ---------"

    except(TypeError,ValueError,AttributeError),e:
        print e
              
    finally:
        print datetime.datetime.now().strftime(dateTimeFormat)
        print "###############Script Completed#################"
        print ""
        if log is not None:
            log.close()