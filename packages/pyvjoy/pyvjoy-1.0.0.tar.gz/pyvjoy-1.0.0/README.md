# pyvjoy

pyvjoy is a set of python binding for <a href='vjoystick.sourceforge.net'>vJoy</a>. This repository is based off <a href="https://github.com/tidzo/pyvjoy">tidzo</a>'s package.

With this library you can easily set Axis and Button values on any vJoy device.  
Low-level bindings are provided in pyvjoy._sdk as well as a (hopefully) slightly more 'Pythonic' API in the pyvjoy.VJoyDevice() object.

Currently vJoyInterface.dll is looked for inside the pyvjoy directory only so place the desired version of that file there to use. (Note: this library currently only works with the x86-64 dll!)


### Requirements

Install vJoy from http://vjoystick.sourceforge.net/site/

After vJoy has installed, copy the vJoyInterface.dll file from your installation location to the location of the python package.

### Installation

1. pip install pyvjoy

### Usage

See examples for simple use cases.

