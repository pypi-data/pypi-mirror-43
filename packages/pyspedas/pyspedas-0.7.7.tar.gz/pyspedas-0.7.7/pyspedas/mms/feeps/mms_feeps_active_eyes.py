'''

 Purpose:
    this function returns the FEEPS active eyes,
    based on date/probe/species/rate

 Output:
    Returns a hash table containing 2 hash tables:
       output['top'] -> maps to the active top eyes
       output['bottom'] -> maps to the active bottom eyes
 
 Notes:
 1) Burst mode should include all sensors (TOP and BOTTOM):
     electrons: [1, 2, 3, 4, 5, 9, 10, 11, 12]
     ions: [6, 7, 8]
 
 2) SITL should return (TOP only):
     electrons: set_intersection([5, 11, 12], active_eyes)
     ions: None
     
 3) From Drew Turner, 9/7/2017, srvy mode:
 
   - before 16 August 2017:
      electrons: [3, 4, 5, 11, 12]
      iond: [6, 7, 8]
 
   - after 16 August 2017:
       MMS1
         Top Eyes: 3, 5, 6, 7, 8, 9, 10, 12
         Bot Eyes: 2, 4, 5, 6, 7, 8, 9, 10

       MMS2
         Top Eyes: 1, 2, 3, 5, 6, 8, 10, 11
         Bot Eyes: 1, 4, 5, 6, 7, 8, 9, 11

       MMS3
         Top Eyes: 3, 5, 6, 7, 8, 9, 10, 12
         Bot Eyes: 1, 2, 3, 6, 7, 8, 9, 10

       MMS4
         Top Eyes: 3, 4, 5, 6, 8, 9, 10, 11
         Bot Eyes: 3, 5, 6, 7, 8, 9, 10, 12

'''

def mms_feeps_active_eyes(trange, probe, data_rate, species, level):
    