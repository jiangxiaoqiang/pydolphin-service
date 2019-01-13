# -*- coding: UTF-8 -*-

import sys
import os.path
import json
sys.path.append("../../../")
print ("OS:"+str(os.path))

from db.ssdb_client import SsdbClient

if __name__ == '__main__': 
    # Using the standard RequestFactory API to create a form POST request
    # SsdbClient.qpush_front(SsdbClient)
    # SsdbClient.qpop_back(SsdbClient)
    str = '{"a":"b"}'
    data = json.loads(str)
    print(data)



