import sys
#sys.path.insert(0, "c:\EnergyPlusV9-5-0")
sys.path.insert(0, "C:\\Projects\\EnergyPlus_dev\\build\\Products\\Release")
from pyenergyplus.api import EnergyPlusAPI

one_time = True
outdoor_temp_sensor = 0
enviroment_diffsolar_actuator = 0
enviroment_directsolar_actuator = 0
enviroment_db_actuator = 0
enviroment_wind_actuator = 0

def time_step_handler(state):
    global one_time, outdoor_temp_sensor, enviroment_diffsolar_actuator, enviroment_db_actuator, enviroment_directsolar_actuator, enviroment_wind_actuator
    sys.stdout.flush()
    if one_time:
        if api.exchange.api_data_fully_ready(state):
            # val = api.exchange.list_available_api_data_csv()
            # with open('/tmp/data.csv', 'w') as f:
            #     f.write(val.decode(encoding='utf-8'))
            outdoor_temp_sensor = api.exchange.get_variable_handle(
                state, u"SITE OUTDOOR AIR DRYBULB TEMPERATURE", u"ENVIRONMENT"
            )
            enviroment_diffsolar_actuator = api.exchange.get_actuator_handle(
                state, "Weather Data", "Diffuse Solar", "Environment"
            )
            enviroment_directsolar_actuator = api.exchange.get_actuator_handle(
                state, "Weather Data", "Direct Solar", "Environment"
            )
            enviroment_wind_actuator = api.exchange.get_actuator_handle(
                state, "Weather Data", "Wind Speed", "Environment"
            )
            enviroment_db_actuator = api.exchange.get_actuator_handle(
                state, "Weather Data", "Outdoor Dry Bulb", "Environment"
            )
            if outdoor_temp_sensor == -1 or enviroment_diffsolar_actuator == -1 or enviroment_db_actuator == -1 or enviroment_directsolar_actuator == -1 or enviroment_wind_actuator == -1:
                sys.exit(1)
            one_time = False
    api.exchange.set_actuator_value(state, enviroment_db_actuator, 22.22)
    api.exchange.set_actuator_value(state, enviroment_wind_actuator, 0)
    api.exchange.set_actuator_value(state, enviroment_directsolar_actuator, 0)
    api.exchange.set_actuator_value(state, enviroment_diffsolar_actuator, 0)
    oa_temp = api.exchange.get_variable_value(state, outdoor_temp_sensor)
    print("Reading outdoor temp via getVariable, value is: %s" % oa_temp)
    sim_time = api.exchange.current_sim_time(state)
    print("Current sim time is: %f" % sim_time)


api = EnergyPlusAPI()
state = api.state_manager.new_state()
api.runtime.callback_begin_zone_timestep_before_set_current_weather(state, time_step_handler)
api.exchange.request_variable(state, "SITE OUTDOOR AIR DRYBULB TEMPERATURE", "ENVIRONMENT")
api.exchange.request_variable(state, "SITE OUTDOOR AIR DEWPOINT TEMPERATURE", "ENVIRONMENT")
# trim off this python script name when calling the run_energyplus function so you end up with just
# the E+ args, like: -d /output/dir -D /path/to/input.idf
api.runtime.run_energyplus(state, sys.argv[1:])