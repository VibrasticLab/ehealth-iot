#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

files = {'file_batuk': open("out.raw","rb")}
values = {'nama': 'pasien', 'gender': 'unknown', 'umur': 0}
req = requests.post("http://103.147.32.57/api/device/sendData/303",files=files, data=values)
#req = requests.post("http://10.124.5.198/api/device/sendData/303",files=files, data=values)