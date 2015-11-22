#!/usr/bin/python
    
import sys
import os
import subprocess
import importlib
from machinekit import launcher
from machinekit import config
from time import *


launcher.register_exit_handler()
launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))
c = config.Config()
os.environ["MACHINEKIT_INI"] = c.MACHINEKIT_INI

try:
    launcher.check_installation()  # make sure the Machinekit installation is sane
    launcher.cleanup_session()  # cleanup a previous session
    # Uncomment and modify the following line if you create a configuration for the BeagleBone Black
    # launcher.load_bbio_file('myoverlay.bbio')  # load a BeagleBone Black universal overlay file
    # Uncomment and modify the following line of you have custom HAL components
    # launcher.install_comp('gantry.comp')  # install a comp HAL component if not already installed
    launcher.install_comp('lineardeltajointscartesian.comp') 
    launcher.start_process("configserver  ~/Machineface ~/Cetus/")  # start the configserver with Machineface an Cetus user interfaces
    launcher.start_process('linuxcnc CRAMPS.ini')  # start linuxcnc
except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)
    
# loop until script receives exit signal
# or one of the started applications exited incorrectly
# cleanup is done automatically
while True:
    sleep(1)
    launcher.check_processes()
