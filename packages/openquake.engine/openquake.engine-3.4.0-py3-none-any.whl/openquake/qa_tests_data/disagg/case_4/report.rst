Disaggregation with sampling
============================

============== ===================
checksum32     1,553,247,118      
date           2019-03-14T01:45:11
engine_version 3.4.0-gita06742ffe6
============== ===================

num_sites = 2, num_levels = 38, num_rlzs = 2

Parameters
----------
=============================== =================
calculation_mode                'disaggregation' 
number_of_logic_tree_samples    2                
maximum_distance                {'default': 40.0}
investigation_time              50.0             
ses_per_logic_tree_path         1                
truncation_level                3.0              
rupture_mesh_spacing            5.0              
complex_fault_mesh_spacing      5.0              
width_of_mfd_bin                0.2              
area_source_discretization      10.0             
ground_motion_correlation_model None             
minimum_intensity               {}               
random_seed                     9000             
master_seed                     0                
ses_seed                        42               
=============================== =================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        0.50000 trivial(1)      1               
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== =================== =========== ======================= =================
grp_id gsims               distances   siteparams              ruptparams       
====== =================== =========== ======================= =================
0      '[ChiouYoungs2008]' rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
====== =================== =========== ======================= =================

Realizations per (GRP, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=2)
  0,'[ChiouYoungs2008]': [0 1]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 1,084        2,236       
================ ====== ==================== ============ ============

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight 
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======
0      2         A    1     5     1,440        2.00494   1.21902    96        96        144    
0      4         C    7     11    164          0.44131   2.02725    10        10        656    
0      1         P    0     1     15           0.00904   2.074E-05  1.00000   1         1.50000
0      3         S    5     7     617          0.0       0.0        0.0       0         0.0    
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    2.00494   1     
C    0.44131   1     
P    0.00904   1     
S    0.0       1     
==== ========= ======

Information about the tasks
---------------------------
================== ======= ======= ======= ======= =======
operation-duration mean    stddev  min     max     outputs
read_source_models 0.03041 NaN     0.03041 0.03041 1      
split_filter       0.24026 NaN     0.24026 0.24026 1      
classical          0.24857 0.47221 0.03159 1.52926 10     
build_hazard_stats 0.00546 0.00285 0.00345 0.00748 2      
================== ======= ======= ======= ======= =======

Fastest task
------------
taskno=4, weight=88, duration=0 s, sources="4"

======== ======= ====== === === =
variable mean    stddev min max n
======== ======= ====== === === =
nsites   1.00000 NaN    1   1   1
weight   88      NaN    88  88  1
======== ======= ====== === === =

Slowest task
------------
taskno=0, weight=99, duration=1 s, sources="4"

======== ======= ====== ======= ======= ==
variable mean    stddev min     max     n 
======== ======= ====== ======= ======= ==
nsites   1.00000 0.0    1       1       66
weight   1.50000 0.0    1.50000 1.50000 66
======== ======= ====== ======= ======= ==

Data transfer
-------------
================== ============================================================== ========
task               sent                                                           received
read_source_models converter=313 B fnames=103 B                                   3.73 KB 
split_filter       srcs=3.4 KB srcfilter=253 B dummy=14 B                         99.16 KB
classical          group=101.82 KB param=8.05 KB src_filter=2.15 KB gsims=1.51 KB 350.9 KB
build_hazard_stats pgetter=5.24 KB hstats=130 B N=28 B individual_curves=26 B     758 B   
================== ============================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total classical          2.48570   2.50391   10    
make_contexts            0.79096   0.0       1,619 
get_poes                 0.43092   0.0       1,084 
total split_filter       0.24026   2.83594   1     
total read_source_models 0.03041   0.68359   1     
aggregate curves         0.01791   0.72266   10    
total build_hazard_stats 0.01092   0.66406   2     
combine pmaps            0.00951   0.66406   2     
managing sources         0.00816   0.0       1     
saving probability maps  0.00637   0.0       1     
store source model       0.00251   0.0       1     
store source_info        0.00227   0.0       1     
saving statistics        0.00215   0.0       2     
compute stats            8.597E-04 0.0       1     
======================== ========= ========= ======