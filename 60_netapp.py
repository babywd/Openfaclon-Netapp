#!/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import os
import re
import sys
import commands
import urllib2, base64
import netsnmp



def main():
    timestamp = int(time.time())
    step = 60
    host_list = ['172.18.16.201','172.18.16.202','172.18.16.203','172.18.16.204','172.17.118.1','172.17.118.2','172.17.118.3','172.17.118.4','172.17.118.5',
                                 '172.17.118.6','172.17.118.7','172.17.118.8','172.20.118.1','172.20.118.2']
    p = []

    monit_keys = [
        ('netapp.cifs.users.connected','.1.3.6.1.4.1.789.1.7.2.9.0'),
        ('netapp.fs.overallstatus','.1.3.6.1.4.1.789.1.5.7.1.0'),
        ('netapp.global.status','.1.3.6.1.4.1.789.1.2.2.4.0'),
        ('netapp.cpu.busy','.1.3.6.1.4.1.789.1.2.1.3.0'),
        ('netapp.cf.status','.1.3.6.1.4.1.789.1.2.3.2.0'),
        ('netapp.cf.setting','.1.3.6.1.4.1.789.1.2.3.1.0'),
        ('netapp.interconnect','.1.3.6.1.4.1.789.1.2.3.8.0'),
        ('netapp.cf.partnerstatus','.1.3.6.1.4.1.789.1.2.3.4.0'),
        ('netapp.disk.failed.count','.1.3.6.1.4.1.789.1.6.4.7.0'),
        ('netapp.disk.prefailed.count','.1.3.6.1.4.1.789.1.6.4.11.0'),
        ('netapp.fan.failed.count','.1.3.6.1.4.1.789.1.2.4.2.0'),
        ('netapp.pw.failed.count','.1.3.6.1.4.1.789.1.2.4.4.0'),
        ('netapp.nvramBatteryStatus','.1.3.6.1.4.1.789.1.2.5.1.0'),
        ('netapp.envOverTemperature','.1.3.6.1.4.1.789.1.2.4.1.0'),
    ]

    for host in host_list:
        for key,oid in monit_keys:
			if key in ['netapp.cpu.busy']:
				version = 2
			else:
				version = 1

			value = netsnmp.snmpget(oid, Version = version, DestHost=host, Community='public')[0]
			i = {
					'Metric':  key,
					'Endpoint': '%s-netapp'%host,
					'Timestamp': timestamp,
					'Step': step,
					'Value': value,
					'CounterType': 'GAUGE',
					'TAGS': 'netapp'
			}
			p.append(i)


    print json.dumps(p, sort_keys=True,indent=4)
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = 'http://172.18.14.5:6060/api/push'
    request = urllib2.Request(url, data=json.dumps(p) )
    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method
    try:
        pass
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    if connection.code == 200:
        print connection.read()
    else:
        print '{"err":1,"msg":"%s"}' % connection

if __name__ == '__main__':
    main()
