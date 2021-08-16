#!/usr/bin/python3
 
from re import I
import sys
import json
import logging
import logging.handlers
from datetime import datetime, time, timedelta

#sys.path.insert(0, 'PyViCare')
from PyViCare.PyViCareGazBoiler import GazBoiler


logger = logging.getLogger('read_heating')
# only the output packet and errors
# logger.setLevel(logging.INFO)

# only errors and warnings
logger.setLevel(logging.WARNING)

# full debug output
logger.setLevel(logging.DEBUG)

# add the correct handler
# console
#handler = logging.StreamHandler()

# Syslog
# handler = logging.handlers.SysLogHandler(address = '/dev/log')
# File
# handler = logging.FileHandler('pyvicare.log', mode='a')
# Console
handler = logging.StreamHandler()
# Null
# handler = logging.NullHandler()

# formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
formatter = logging.Formatter('%(module)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

now = datetime.now()
epoch = now.strftime("%s")

logger.debug ("==== "+str(now)+" ===========================================================================")

# get all values at once
try:
    t=GazBoiler("username@mail.de","123456","123sed45t6","token.save")
    logger.debug("Connection Result:=%s" % t)
except:
    logger.critical("Connection Error:=%s" % t)
    sys.exit(1)

# get all in one request
result = t.getAllEntries()

# count all data entries
try:
    data_count = len(result['data'])
    logger.debug ("Data Count:"+str(data_count))
except:
    logger.critical("Result:=%s" % result)
    sys.exit(1)

# heating circuit is allways 0
# handle every entry individually
# beware of longer matches
# possible HeatingProgram
dict_HeatingProgram = { 'standby': 0, 'reduced': 1, 'normal': 2, 'comfort': 3 , 'forcedLastFromSchedule': 4, 'screedDrying': 5, 'active': 6 }

# default values
HeatingTimeOffset = 0
HeatingProgram_string = ''
HeatingProgram = 0
HeatingOutsideTemperature = 0
HeatingDesiredTemperature = 3
Shift = 0
Slope = 1
HeatingSupplyTemperatureTarget = 20
HeatingSupplyTemperature = 20
HeatingDHWTemperatureMain = 60
HeatingDHWTemperatureHygiene = 70
HeatingDHWTemperatureTarget = 60
HeatingDHWTemperature = 20
# heating or dhw
HeatingMode = 'heating'
HeatingBurnerStatus = 'False'
HeatingBurnerModulation = 0
HeatingBurnerModulationHeating = 0
HeatingBurnerModulationDHW = 0
HeatingCirculationPump = 'off'
HeatingDHWCirculationPump = 'fake'
HeatingGasConsumptionHeating = 0
HeatingGasConsumptionDHW = 0
HeatingPowerConsumption = 0
HeatingBurnerHours = 0
HeatingBurnerStarts = 0
HeatingSupplyPressure = 0

# extra run to get HeatingProgram, TimeOffset, HeatingMode
for feature_number in range(data_count) :
    feature = str(result['data'][feature_number]['feature'])
    # ("heating.circuits.0.operating.programs.active")["properties"]["value"]["value"]
    device_feature = 'heating.circuits.0.operating.programs.active'
    if device_feature == feature :
        HeatingProgram_string = result['data'][feature_number]['properties']['value']['value']
        HeatingProgram = dict_HeatingProgram.get(HeatingProgram_string)
        logger.debug (device_feature + ' : ' + HeatingProgram_string + ':' + str(HeatingProgram))

    # ("heating.device.time.offset")["properties"]["value"]["value"
    device_feature = 'heating.device.time.offset'
    if device_feature == feature :
        HeatingTimeOffset = result['data'][feature_number]['properties']['value']['value']
        logger.debug (device_feature + ' : ' + str(HeatingTimeOffset))

    # ("heating.valves.diverter.heatDhw")["properties"]["position"]["value"]
    device_feature = 'heating.valves.diverter.heatDhw'
    if device_feature == feature :
        HeatingMode = str(result['data'][feature_number]['properties']['position']['value'])
        logger.debug (device_feature + ' : ' + HeatingMode)

midnight = datetime.combine(datetime.today(), time.min)
midnight_offset = midnight + timedelta(minutes=int(HeatingTimeOffset))
logger.debug ( str(midnight) + " " + str(midnight_offset) )

for feature_number in range(data_count) :
    feature = str(result['data'][feature_number]['feature'])
    
    # ("heating.sensors.temperature.outside")["properties"]["value"]["value"]
    device_feature = 'heating.sensors.temperature.outside'
    if device_feature == feature :
        HeatingOutsideTemperature = result['data'][feature_number]['properties']['value']['value']
        logger.debug (device_feature + ' : ' + str(HeatingOutsideTemperature))

    # ("heating.circuits.0.operating.programs.HeatingProgram")["properties"]["temperature"]["value"]
    # fallback value for desired temp
    device_feature = 'heating.circuits.0.operating.programs.'+HeatingProgram_string
    if device_feature == feature :
        try :
            HeatingDesiredTemperature = result['data'][feature_number]['properties']['temperature']['value']
        except :
            HeatingDesiredTemperature = 3
        logger.debug (device_feature + ' : ' + "HeatingDesiredTemperature" + ' : ' + str(HeatingDesiredTemperature))
    # ("heating.circuits.0.heating.curve")["properties"]["shift"]["value"]
    # ("heating.circuits.0.heating.curve")["properties"]["slope"]["value"]
    device_feature = 'heating.circuits.0.heating.curve'
    if device_feature == feature :
        Shift = result['data'][feature_number]['properties']['shift']['value']
        Slope = result['data'][feature_number]['properties']['slope']['value']
        logger.debug (device_feature + ' : ' + "Shift" + ' : ' + str(Shift))
        logger.debug (device_feature + ' : ' + "Slope" + ' : ' + str(Slope))

    # Calculates target supply temperature based on data from Viessmann
    # See: https://www.viessmann-community.com/t5/Gas/Mathematische-Formel-fuer-Vorlauftemperatur-aus-den-vier/m-p/68890#M27556
    delta_outside_inside = HeatingOutsideTemperature - HeatingDesiredTemperature
    HeatingSupplyTemperatureTarget = round((HeatingDesiredTemperature + Shift - Slope * delta_outside_inside * (1.4347 + 0.021 * delta_outside_inside + 247.9 * pow(10, -6) * pow(delta_outside_inside, 2))),1)
    # less than 20 makes no sense, fallback to minimal 20 supply temp
    if HeatingSupplyTemperatureTarget < 20 :
        HeatingSupplyTemperatureTarget = 20

    # ("heating.circuits.0.sensors.temperature.supply")["properties"]["value"]["value"]
    # ("heating.boiler.sensors.temperature.commonSupply"["properties"]["value"]["value"]
    device_feature = 'heating.boiler.sensors.temperature.commonSupply'
    if device_feature == feature :
        HeatingSupplyTemperature = result['data'][feature_number]['properties']['value']['value']
        logger.debug (device_feature + ' : ' + str(HeatingSupplyTemperature))
        logger.debug ('HeatingSupplyTemperatureTarget' + ' : ' + str(HeatingSupplyTemperatureTarget))

    # ("heating.dhw.temperature.main")["properties"]["value"]["value"]
    # the normal temperature here
    device_feature = 'heating.dhw.temperature.main'
    if device_feature == feature :
        HeatingDHWTemperatureMain = result['data'][feature_number]['properties']['value']['value']
        logger.debug ("'HeatingDHWTemperatureMain'" + ' : ' + str(HeatingDHWTemperatureMain))

    # ("heating.dhw.temperature.hygiene")["properties"]["value"]["value"]
    # the normal temperature here
    device_feature = 'heating.dhw.temperature.hygiene'
    if device_feature == feature :
        HeatingDHWTemperatureHygiene = result['data'][feature_number]['properties']['value']['value']
        logger.debug ("'HeatingDHWTemperatureHygiene'" + ' : ' + str(HeatingDHWTemperatureHygiene))

    # for simplicity set target == main
    HeatingDHWTemperatureTarget = HeatingDHWTemperatureMain
    logger.debug ("'HeatingDHWTemperatureTarget'" + ' : ' + str(HeatingDHWTemperatureTarget))

    # ("heating.dhw.sensors.temperature.hotWaterStorage")["properties"]["value"]["value"]
    device_feature = 'heating.dhw.sensors.temperature.hotWaterStorage'
    if device_feature == feature :
        HeatingDHWTemperature = result['data'][feature_number]['properties']['value']['value']
        logger.debug (device_feature + ' : ' + str(HeatingDHWTemperature))

   # ("heating.burner")["properties"]["active"]["value"]
    device_feature = 'heating.burner'
    if device_feature == feature :
        HeatingBurnerStatus = str(result['data'][feature_number]['properties']['active']['value'])
        logger.debug (device_feature + ' : ' + HeatingBurnerStatus)

    # ('heating.burners.0.modulation')["properties"]["value"]["value"]
    device_feature = 'heating.burners.0.modulation'
    if device_feature == feature :
        HeatingBurnerModulation = result['data'][feature_number]['properties']['value']['value']
        if HeatingMode == "heating"  :
            HeatingBurnerModulationHeating = HeatingBurnerModulation
        if HeatingMode == "dhw"  :
            HeatingBurnerModulationDHW = HeatingBurnerModulation
        logger.debug (device_feature + ' Modulation/Heating/DHW : ' + str(HeatingBurnerModulation) + '/' + str(HeatingBurnerModulationHeating) + '/' + str(HeatingBurnerModulationDHW))

    # ("heating.circuits.0.circulation.pump")["properties"]["status"]["value"]
    device_feature = 'heating.circuits.0.circulation.pump'
    if device_feature == feature :
        HeatingCirculationPump = str(result['data'][feature_number]['properties']['status']['value'])
        logger.debug (device_feature + ' : ' + HeatingCirculationPump )

    # ("heating.dhw.pumps.primary")["properties"]["status"]["value"]
    device_feature = 'heating.dhw.pumps.circulation'
    if device_feature == feature :
        HeatingDHWCirculationPump = str(result['data'][feature_number]['properties']['status']['value'])
        logger.debug (device_feature + ' : ' + HeatingDHWCirculationPump )

    # ('heating.gas.consumption.heating')['properties']['day']['value'][0]
    device_feature = 'heating.gas.consumption.heating'
    if device_feature == feature :
        # value is only time offset after midnight valid
        # if now > midnight_offset :
        HeatingGasConsumptionHeating = result['data'][feature_number]['properties']['day']['value'][0]
        logger.debug (device_feature + ' : ' + str(HeatingGasConsumptionHeating) )

    # ('heating.gas.consumption.dhw')['properties']['day']['value'][0]
    device_feature = 'heating.gas.consumption.dhw'
    if device_feature == feature :
        if now > midnight_offset :
            HeatingGasConsumptionDHW = result['data'][feature_number]['properties']['day']['value'][0]
        logger.debug (device_feature + ' : ' + str(HeatingGasConsumptionDHW) )

    # 'heating.power.consumption')['properties']['day']['value'][0]
    device_feature = 'heating.power.consumption'
    if device_feature == feature :
        try :
            if now > midnight_offset :
                HeatingPowerConsumption = result['data'][feature_number]['properties']['day']['value'][0]
        except :
            HeatingPowerConsumption = 0
        logger.debug (device_feature + ' : ' + str(HeatingPowerConsumption) )

    # ('heating.burners.0.statistics')['properties']['hours']['value'
    # ('heating.burners.0.statistics')['properties']['starts']['value'
    device_feature = 'heating.burners.0.statistics'
    if device_feature == feature :
        HeatingBurnerHours = str(result['data'][feature_number]['properties']['hours']['value'])
        HeatingBurnerStarts = str(result['data'][feature_number]['properties']['starts']['value'])
        logger.debug (device_feature + ' : ' + "hours" + ' : ' + HeatingBurnerHours )
        logger.debug (device_feature + ' : ' + "starts" + ' : ' + HeatingBurnerStarts )

    # ('heating.sensors.pressure.supply')['properties']['value']['value']
    device_feature = 'heating.sensors.pressure.supply'
    if device_feature == feature :
        HeatingSupplyPressure = str(result['data'][feature_number]['properties']['value']['value'])
        logger.debug (device_feature + ' : ' + HeatingSupplyPressure )

logger.debug ("====================================================================================================")

# fake modulation
# if HeatingBurnerStatus == 'True' :
#     HeatingBurnerModulationHeating = 50

# first the epoch and some stats
logger.debug("epoch=%s,HeatingProgram=%s,HeatingBurnerModulationHeating=%s,HeatingBurnerModulationDHW=%s" % (epoch, HeatingProgram, HeatingBurnerModulationHeating, HeatingBurnerModulationDHW))

logger.debug("----------------------------------------------------------------------------------------------------")

# Heating Temperatures
logger.debug("HeatingOutsideTemperature=%s,HeatingDesiredTemperature=%s,HeatingSupplyTemperatureTarget=%s,HeatingSupplyTemperature=%s" % (HeatingOutsideTemperature, HeatingDesiredTemperature, HeatingSupplyTemperatureTarget, HeatingSupplyTemperature))
logger.debug("----------------------------------------------------------------------------------------------------")

# DHW Temperartures
logger.debug("HeatingDHWTemperatureTarget=%s,HeatingDHWTemperature=%s" % (HeatingDHWTemperatureTarget, HeatingDHWTemperature))
logger.debug("----------------------------------------------------------------------------------------------------")

# Consumptions
logger.debug("HeatingGasConsumptionHeating=%s,HeatingGasConsumptionDHW=%s,HeatingPowerConsumption=%s" % (HeatingGasConsumptionHeating, HeatingGasConsumptionDHW, HeatingPowerConsumption))
logger.debug("----------------------------------------------------------------------------------------------------")

# Burner Statistics and pressure
logger.debug("HeatingBurnerHours=%s,HeatingBurnerStarts=%s,HeatingSupplyPressure=%s" % (HeatingBurnerHours, HeatingBurnerStarts, HeatingSupplyPressure))

logger.debug ("====================================================================================================")

# build the output
# my_file='/var/www/html/heating/viessmann'
my_file='viessmann'
try:
    fp = open(my_file, 'w')
    logger.info ("epoch=%s,HeatingProgram=%s,HeatingBurnerModulationHeating=%s,HeatingBurnerModulationDHW=%s,HeatingOutsideTemperature=%s,HeatingDesiredTemperature=%s,HeatingSupplyTemperatureTarget=%s,HeatingSupplyTemperature=%s,HeatingDHWTemperatureTarget=%s,HeatingDHWTemperature=%s,HeatingGasConsumptionHeating=%s,HeatingGasConsumptionDHW=%s,HeatingPowerConsumption=%s,HeatingBurnerHours=%s,HeatingBurnerStarts=%s,HeatingSupplyPressure=%s" % (epoch, HeatingProgram, HeatingBurnerModulationHeating, HeatingBurnerModulationDHW, HeatingOutsideTemperature, HeatingDesiredTemperature, HeatingSupplyTemperatureTarget, HeatingSupplyTemperature, HeatingDHWTemperatureTarget, HeatingDHWTemperature, HeatingGasConsumptionHeating, HeatingGasConsumptionDHW, HeatingPowerConsumption, HeatingBurnerHours, HeatingBurnerStarts, HeatingSupplyPressure))
    fp.write ("epoch=%s,HeatingProgram=%s,HeatingBurnerModulationHeating=%s,HeatingBurnerModulationDHW=%s,HeatingOutsideTemperature=%s,HeatingDesiredTemperature=%s,HeatingSupplyTemperatureTarget=%s,HeatingSupplyTemperature=%s,HeatingDHWTemperatureTarget=%s,HeatingDHWTemperature=%s,HeatingGasConsumptionHeating=%s,HeatingGasConsumptionDHW=%s,HeatingPowerConsumption=%s,HeatingBurnerHours=%s,HeatingBurnerStarts=%s,HeatingSupplyPressure=%s" % (epoch, HeatingProgram, HeatingBurnerModulationHeating, HeatingBurnerModulationDHW, HeatingOutsideTemperature, HeatingDesiredTemperature, HeatingSupplyTemperatureTarget, HeatingSupplyTemperature, HeatingDHWTemperatureTarget, HeatingDHWTemperature, HeatingGasConsumptionHeating, HeatingGasConsumptionDHW, HeatingPowerConsumption, HeatingBurnerHours, HeatingBurnerStarts, HeatingSupplyPressure))
    fp.close()
except:
    logger.critical("Can't write to %s " % my_file )
