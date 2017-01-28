import re

def determine_os(output):
    if re.search('Cisco IOS Software, IOS-XE Software', output):
        os = 'iosxe'
    elif re.search('Cisco IOS XR Software', output):
        os = 'iosxr'
    elif re.search('Cisco IOS Software, .*\d{2,5}.* Software', output):
        os = 'ios'
    elif re.search('Cisco Internetwork Operating System Software', output):
        os = 'ios'
    elif re.search('Cisco Nexus Operating System \(NX-OS\) Software', output):
        os = 'nxos'
    elif re.search('Cisco Adaptive Security Appliance Software', output):
        os = 'asa'
    elif re.search('ASA', output):
        os = 'asa'
    elif re.search('FWSM Firewall', output):
        os = 'fwsm'
    elif re.search('Cisco PIX Security Appliance Software', output):
        os = 'pix'
    elif re.search('Arista', output):
        os = 'eos'
    else:
        os = 'unknown'
    return os

class FilterModule(object):
    def filters(self):
        return {
            'determine_os': determine_os,
        }
