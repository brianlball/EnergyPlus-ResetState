import matplotlib.pyplot as plt
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
    global count, one_time, outdoor_temp_sensor, enviroment_diffsolar_actuator, enviroment_db_actuator, enviroment_directsolar_actuator, enviroment_wind_actuator
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
    if count > 200:
        api.exchange.set_actuator_value(state, enviroment_db_actuator, 26.00)
    else:
        api.exchange.set_actuator_value(state, enviroment_db_actuator, 22.22)

    api.exchange.set_actuator_value(state, enviroment_wind_actuator, 0)
    api.exchange.set_actuator_value(state, enviroment_directsolar_actuator, 0)
    api.exchange.set_actuator_value(state, enviroment_diffsolar_actuator, 0)
    oa_temp = api.exchange.get_variable_value(state, outdoor_temp_sensor)
    zone_temp_handle = api.exchange.get_variable_handle(state, "Zone Mean Air Temperature", 'Zone One')
    print("Reading outdoor temp via getVariable, value is: %s" % oa_temp)
    sim_time = api.exchange.current_sim_time(state)
    print("Current sim time is: %f" % sim_time)
    
    count += 1
    x.append(count)
    y_outdoor.append(oa_temp)
    zone_temp = api.exchange.get_variable_value(state, zone_temp_handle)
    y_zone.append(zone_temp)
    if count % plot_update_interval == 0:
        update_line()

#plotting
hl, = plt.plot([], [], label="Outdoor Air Temp")
h2, = plt.plot([], [], label="Zone Temperature")
ax = plt.gca()
plt.title('Outdoor Temperature')
plt.xlabel('Zone time step index')
plt.ylabel('Temperature [C]')
plt.legend(loc='lower right')
x = []
y_outdoor = []
y_zone = []
count = 0
plot_update_interval = 250  # time steps

def update_line():
    hl.set_xdata(x)
    hl.set_ydata(y_outdoor)
    h2.set_xdata(x)
    h2.set_ydata(y_zone)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.00001)




api = EnergyPlusAPI()
state = api.state_manager.new_state()
api.runtime.callback_begin_zone_timestep_before_set_current_weather(state, time_step_handler)
#api.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, time_step_handler)
#api.exchange.request_variable(state, "SITE OUTDOOR AIR DRYBULB TEMPERATURE", "ENVIRONMENT")
#api.exchange.request_variable(state, "SITE OUTDOOR AIR DEWPOINT TEMPERATURE", "ENVIRONMENT")
# trim off this python script name when calling the run_energyplus function so you end up with just
# the E+ args, like: -d /output/dir -D /path/to/input.idf
#api.runtime.run_energyplus(
#    state,
#    [
#        '-a',
#        '-w', '/Users/mmitchel/Projects/EnergyPlus/dev/develop/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw',
#        '-d', '/Users/mmitchel/Projects/demoeplusapi/dump',
#        '/Users/mmitchel/Projects/EnergyPlus/dev/develop/testfiles/' + filename_to_run
#    ]
#)
#TODO
#case 1. load a state from file, set state, and start running.
# LOAD STATE FROM DISK
#loaded_state = api.state_manager.load_state(:FilePath)  #make sure it fills out all data structures.

#api.runtime.set_state(loaded_state)  # probably have to set output files, reopen them and append the outputs. so do this... maybe. pythonplugin?
#api.runtime.run_energyplus(loaded_state, sys.argv[1:])
#OR
#api.runtime.continue_energyplus(loaded_state, sys.argv[1:])  #which would do the above maintenance.  reopen input files, in sim manager
#check points for the enpoints of a run.

# only save state at end of day.
#leave sim manager
#

# skip first parts of sim manager so you can dive back into it.
# can you reorg it so you enter and exit it cleanly?   so it handles the files, etc

#1. stop sim manager, save outputs files, start it again, open files, continue run.
#2. save state, same as above.
#3. state file struct, APIs

#TODO
#case 2. get an object, change its value in state and then start running (warmup or no?).
# GET AN OBJECT IN A STATE
#object_state = api.state.get_state(state, object_name) ##is object_name unique?
# LIST THE MEMBERS OF OBJECT
#api.state_manager.list_members(object_State)
# CHANGE THE VALUE OF A MEMEBER 
#api.state_manager.change_state(object_state, key, value)
# MERGE THE NEW STATE INTO STATE
#api.runtime.state_manager.merge_state(state, object_state)
# RUN
#api.runtime.run_energyplus(state, sys.argv[1:]) :NoWarmup or :SetTimeToSomething ?


#CASE 3   no existing state.  but still set values in state for objects.
# normal start.  change state (actuator value example.  E+ starts immediately with those values.  new calling point?  no warmup, or dds.  

api.runtime.run_energyplus(state, sys.argv[1:])

plt.show()
