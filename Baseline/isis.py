#! /usr/bin/env python
 

import sys, Baseline_Module

print(sys.argv)
Baseline_Module.bgp_check_db(sys.argv[1])
Baseline_Module.isis_check_db(sys.argv[1])
Baseline_Module.isis_check_with_conf(sys.argv[1])
