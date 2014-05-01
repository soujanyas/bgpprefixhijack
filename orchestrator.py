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
       table['cyc_tp'] = cyclops_capture.has_transient_prefix_anam(from_time, to_time, a_res)
       table['cyc_dp'] = cyclops_capture.has_depeering_anam(from_time, to_time, a_res)
       table['cyc_ba'] = cyclops_capture.has_bogus_asn_anam(from_time, to_time, a_res)
       table['cyc_bp'] = cyclops_capture.has_bogon_prefix_anam(from_time, to_time, a_res)
       table['cyc_pl'] = cyclops_capture.has_prefix_len_anam(from_time, to_time, a_res)
       table_list.append(table)
    print ("-------------------------------------------------------------------")
    print ("cyc_tp\tcyc_dp\tcyc_ba\tcyc_bp\tcyc_pl\tas_path/origin\t\t ")
    print ("-------------------------------------------------------------------")
    for table in table_list:
      print ("%s\t%s\t%s\t%s\t%s\t%s" % (table['cyc_tp'], table['cyc_dp'], table['cyc_ba'], table['cyc_bp'], table['cyc_pl'], table['as']))

       #nether_capture.get_results(a_res)
        

    
