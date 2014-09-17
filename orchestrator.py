#!/usr/bin/python3

'''
Python module to capture BGP hijack data when multiple approaches are
chained together
'''

from cyclops.cyclops_capture import CyclopsCapture
from nether.nether_capture import NetherCapture
from argus.a_capture import ArgusCapture
from conchijack.conc_hijack_capture import ConcHijackCapture
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--count_table", help="Get count table for the date ranges")
parser.add_argument("--consolidation_table", help="Get consolidation table for the date ranges")

from_time = "2014-04-23"
to_time = "2014-05-01"

time_list = [{"from_time": "2013-07-01", "to_time": "2013-07-07"},
             {"from_time": "2013-07-08", "to_time": "2013-07-14"},
             {"from_time": "2013-07-15", "to_time": "2013-07-21"},
             {"from_time": "2013-07-22", "to_time": "2013-07-30"}]

#time_list = [{"from_time": "2013-07-01", "to_time": "2013-07-07"},
#             {"from_time": "2013-07-08", "to_time": "2013-07-14"}]

def calculate_score(table):
  return list(table.values()).count(True)

def make_count_table():
    argus_capture = ArgusCapture()
    cyclops_capture = CyclopsCapture()
    nether_capture = NetherCapture()
    concurrent_capture = ConcHijackCapture()
    table_list = list()

    for time in time_list:

       table = dict()
       from_time = table["from"] = time["from_time"]
       to_time = table["to"] = time["to_time"]
       table['argus'] = len(argus_capture.get_alarms_in_range(from_time, to_time))
       table['cyc_tp'] = cyclops_capture.count_transient_prefix_anam(from_time, to_time)
       table['cyc_dp'] = cyclops_capture.count_depeering_anam(from_time, to_time)
       table['cyc_ba'] = cyclops_capture.count_bogus_asn_anam(from_time, to_time)
       table['cyc_bp'] = cyclops_capture.count_bogon_prefix_anam(from_time, to_time)
       table['cyc_pl'] = cyclops_capture.count_prefix_len_anam(from_time, to_time)
       table['nether'] = nether_capture.count_nether_anam(from_time, to_time)
       table['conc_hijack'] = concurrent_capture.count_conc_hijack_anam(from_time, to_time)
       table_list.append(table)

    print ("\n")
    print ("--------------------------------------------------------------------------------------------------------")
    print ("time\t\t\targus\tcyc_tp\tcyc_dp\tcyc_ba\tcyc_bp\tcyc_pl\tnether\tconc_hijack")
    print ("--------------------------------------------------------------------------------------------------------")
    for table in table_list:
      print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (table["from"] + "->" + table["to"],
                                             table['argus'],
                                             table['cyc_tp'], table['cyc_dp'],
                                             table['cyc_ba'], table['cyc_bp'],
                                             table['cyc_pl'], table['nether'],
                                             table['conc_hijack']
                                             ))
    print ("\n")

def make_consolidation_table():
    argus_capture = ArgusCapture()
    cyclops_capture = CyclopsCapture()
    nether_capture = NetherCapture()

    table_list = list()
    argus_res = argus_capture.get_alarms_in_range(from_time, to_time)
    count = 0

    for a_res in argus_res:
       table = dict()
       table['as'] = a_res['origin'] + a_res['bad_path_segment']
       table['prefix'] = a_res['prefix']
       table['argus'] = True
       table['cyc_tp'] = cyclops_capture.has_transient_prefix_anam(from_time, to_time, a_res)
       table['cyc_dp'] = cyclops_capture.has_depeering_anam(from_time, to_time, a_res)
       table['cyc_ba'] = cyclops_capture.has_bogus_asn_anam(from_time, to_time, a_res)
       table['cyc_bp'] = cyclops_capture.has_bogon_prefix_anam(from_time, to_time, a_res)
       table['cyc_pl'] = cyclops_capture.has_prefix_len_anam(from_time, to_time, a_res)
       table['nether'] = nether_capture.has_nether_anam(from_time, to_time, a_res)
       table['conc_hijack'] = ( concurrent_capture.count_conc_hijack_anam(from_time, to_time) > 0 )
       table['score'] = calculate_score(table)
       table_list.append(table)
       count += 1
    print ("")
    print ("--------------------------------------------------------------------------------------------------------")
    print ("argus\tcyc_tp\tcyc_dp\tcyc_ba\tcyc_bp\tcyc_pl\tnether\tconc\tscore/8\t prefix\t\tas_path/origin\t\t ")
    print ("--------------------------------------------------------------------------------------------------------")
    for table in table_list:
      print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s" % (table['argus'],
                                             table['cyc_tp'], table['cyc_dp'],
                                             table['cyc_ba'], table['cyc_bp'],
                                             table['cyc_pl'], table['nether'],
                                             table['conc_hijack'],
                                             table['score'], table['prefix'],
                                             table['as']))
    print ("\n")

if __name__ == "__main__":
  args = parser.parse_args()
  if(args.consolidation_table == 'True'):
    print ("Making consolidation table")
    make_consolidation_table()

  if(args.count_table == 'True'):
    print ("Making count table")
    make_count_table()

  #print (args)
