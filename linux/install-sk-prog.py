
# -*- coding: utf-8 -*-
"""
Installs SK-Prog keyboard on Linux.

Modifies /usr/share/X11/xkb/symbols/sk with the content from sk-prog file
and /usr/share/X11/xkb/rules/evdev.xml

Needs to be run as superuser:
sudo python3 install-sk-prog.py
"""

import xml.etree.ElementTree as ET
import os, shutil


SK_PATH = '/usr/share/X11/xkb/symbols/sk'
SKPROG_PATH = 'sk-prog'

class SkException(Exception):
    pass


try:
    with open(SK_PATH, 'r') as file:
        con = file.read()
        file.close()
    
    if con.find('xkb_symbols "sk-prog"') != -1:
        raise SkException()
        
    with open(SKPROG_PATH, 'r') as file:
        skprog = file.read()
        file.close()

    if not os.path.isfile(SK_PATH + '.backup'):
        shutil.copyfile(SK_PATH,SK_PATH + '.backup')
        print('backupfile created ' + SK_PATH + '.backup',)
    
    with open(SK_PATH, 'a') as file:
        file.write('\n' + skprog)
    print(SK_PATH, "written")
    
except SkException:
    print('SK-Prog already installed in ' + SK_PATH)


EVDEV_PATH = '/usr/share/X11/xkb/rules/evdev.xml'

skProgXml = """
<variant>
  <configItem>
    <name>sk-prog</name>
    <shortDescription>sk-prog</shortDescription>
    <description>Slovak (Prog)</description>
  </configItem>
</variant>
"""

headXml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xkbConfigRegistry SYSTEM "xkb.dtd">
"""

class EvdevException(Exception):
    pass

try:
    tree = ET.parse(EVDEV_PATH)
    root = tree.getroot()
    
    VL = root.find("./layoutList/layout/configItem/[name='sk']/../variantList")
    skProgEl = VL.find("./variant/configItem/[name='sk-prog']")
    
    if skProgEl is not None:
        raise EvdevException()
    
    VL.append(ET.fromstring(skProgXml))


    if not os.path.isfile(EVDEV_PATH + '.backup'):
        shutil.copyfile(EVDEV_PATH, EVDEV_PATH + '.backup')
        print('backupfile created ' + EVDEV_PATH + '.backup')


    tree.write(EVDEV_PATH)
    with open(EVDEV_PATH, "r+") as file:
        fileXml = file.read()
        file.seek(0)
        file.write(headXml + fileXml)
        
    print(EVDEV_PATH, "written")
    
except EvdevException:
    print("sk-prog already in evdev.xml")


print("Installed")