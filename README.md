==============
DemoServos
==============

This demo application demonstrate actuating servo motors using Phidgets (http://www.phidgets.com/) modules.


Dependencies
============

* Phidgets libraries (Follow instructions at: http://www.phidgets.com/docs/Operating_System_Support)
* Phidgets Python Module (Found at utils/PhidgetsPython. Download and install with *python setup.py install*)
* Python scripts in this repository depend on the existence of the *Phidgets* folder in this repository.

Running the sensors
===================

You first need to change the SERV_USER and SERV_PASS variables in the *demo-servos.py* file, assing your username and password, or key and secret generated here: http://wotkit.sensetecnic.com/wotkit/keys. To run the script, run (in ubuntu you need to run with superuser privileges):

```
sudo python phidgetrelay.py
```
In rare cases, if you are using a different WoTKit API end-point, you can configure the *STS_BASE_URL='http://wotkit.sensetecnic.com/api'* variable to your desired end point.

