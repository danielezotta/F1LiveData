# F1 Live Data

This repo is about Formula One Data, containing for now only a quali lap steering wheel representation.

## Run
Simply run 

`pip install fastf1 kivy`

for depencecies, then run

`python main.py`
 
and you are good to go

## Options

### Qualification steering sheel

![Alt text](preview/quali_steering_wheel_preview.gif?raw=true "Option preview")

Shows the steering wheel of the selected driver and circuit for the quali lap, with the informations available. 
As it stands, the steering wheel is the one from the Ferrari F1-75.

Things not working (mostly because not found in database):
- tyre temperature
- brake balance
- session time
- state of charge

### Qualification circuit comparison (still alpha)

Shows a map with the circuit and two dots representing the two drivers selected for the qualifying. 
For now is lagging between samples, but the objective is to move them smoothly.

### Race speed comparison

![Alt text](preview/race_speed_comparison_preview.png?raw=true "Option preview")

Shows all the registered speeds for two drivers during the selected race, lap by lap.
The speedtraps names are:
- SpeedI1 : speedtrap at the intermediate 1
- SpeedI2 : speedtrap at the intermediate 2
- SpeedFL : speedtrap at the finish line
- SpeedST : speedtrap at the intermediate 1

The averages are computed on all not nan values, for each driver.