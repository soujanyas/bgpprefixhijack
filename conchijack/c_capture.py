'''
Python module to capture and analyze data for concurrent prefix hijacks
'''

from pybgpdump import BGPDump

filename = "sample/updates.20011026.1322.bz2"

if __name__ == "__main__":
    dump = BGPDump(filename);
    count = 0
    (pkt1, pkt2, pkt3) =  dump.next()
    try:
        while pkt3:
	    #print (pkt3)
            count += 1
            pkt3 = dump.next()
            print(dump)
        for mrt_h, bgp_h, bgp_m in dump:
    	    print ("here1")
            origin = as_path = next_hop = multi_exit_disc = local_pref = \
            atomic_aggregate = aggregator = originator_id = cluster_list = \
            communities = None
            for attr in bgp_m.update.attributes:
                if attr.type == bgp.ORIGIN:
                    origin = origin_to_str(attr.origin)
                elif attr.type == bgp.AS_PATH:
                    as_path = aspath_to_str(attr.as_path)
                elif attr.type == bgp.NEXT_HOP:
                    next_hop = dnet.ip_ntoa(attr.next_hop.ip)
                elif attr.type == bgp.MULTI_EXIT_DISC:
                    multi_exit_disc = '%d' % (attr.multi_exit_disc.value)
                elif attr.type == bgp.LOCAL_PREF:
                    local_pref = '%d' % (attr.local_pref.value)
                elif attr.type == bgp.ATOMIC_AGGREGATE:
                    atomic_aggregate = 'AG'
                elif attr.type == bgp.ORIGINATOR_ID:
                    originator_id = dnet.ip_ntoa(attr.originator_id.value)
                elif attr.type == bgp.CLUSTER_LIST:
                    cluster_list = clusterlist_to_str(attr.cluster_list)
                elif attr.type == bgp.COMMUNITIES:
                    communities = communities_to_str(attr.communities)

            out('TIME: %s\n' %
                (time.strftime('%D %T', time.localtime(mrt_h.ts))))
            out('TYPE: BGP4MP/MESSAGE/Update\n')
            out('FROM: %s AS%d\n' % (dnet.ip_ntoa(bgp_h.src_ip), bgp_h.src_as))
            out('TO: %s AS%d\n' % (dnet.ip_ntoa(bgp_h.dst_ip), bgp_h.dst_as))
            if origin:
                out('ORIGIN: %s\n' % (origin))
            if as_path:
                out('ASPATH: %s\n' % (as_path))
            if next_hop:
                out('NEXT_HOP: %s\n' % (next_hop))
            if multi_exit_disc:
                out('MULTI_EXIT_DISC: %s\n' % (multi_exit_disc))
            if local_pref:
                out('LOCAL_PREF: %s\n' % (local_pref))
            if atomic_aggregate:
                out('ATOMIC_AGGREGATE\n')
            if aggregator:
                out('AGGREGATOR: %s\n' % (aggregator))
            if originator_id:
                out('ORIGINATOR_ID: %s\n' % (originator_id))
            if cluster_list:
                out('CLUSTER_LIST: %s\n' % (cluster_list))
            if communities:
                out('COMMUNITY: %s\n' % (communities))

            if len(bgp_m.update.announced) > 0:
                out('ANNOUNCE\n')
                for route in bgp_m.update.announced:
                    out('  %s/%d\n' % (dnet.ip_ntoa(route.prefix), route.len))

            if len(bgp_m.update.withdrawn) > 0:
                out('WITHDRAW\n')
                for route in bgp_m.update.withdrawn:
                    out('  %s/%d\n' % (dnet.ip_ntoa(route.prefix), route.len))

            out('\n')

    except StopIteration:
        print "count = %d" % count
