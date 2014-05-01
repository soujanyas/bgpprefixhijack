#!/usr/bin/python3

'''
Python module to capture BGP hijack data when multiple approaches are
chained together
'''

import urllib.request
from cyclops.cyclops_capture import CyclopsCapture
from argus.a_capture import ArgusCapture

from_time = "2014-04-23"
to_time = "2014-05-01"

if __name__ == "__main__":

    argus_capture = ArgusCapture()
    cyclops_capture = CyclopsCapture()
    #nether_capture = NetherCapture()

    table_list = list()
    argus_res = argus_capture.get_alarms_in_range(from_time, to_time)

    for a_res in argus_res:
       table = dict()
       table['as'] = a_res['origin'] + a_res['bad_path_segment']
       table['cyclops'] = cyclops_capture.has_transient_results(from_time, to_time, a_res)
       table_list.append(table)

    print (table_list)
       #nether_capture.get_results(a_res)
        

    
