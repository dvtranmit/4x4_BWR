4x4_BWR                         Version 1.0.0                      Nov. 15 2013
===============================================================================



===============================================================================
                         AUTHORS & CONTACT INFORMATION
===============================================================================

Undergraduate Contributors-----------------------------------------------------

        Stephanie Pavlick -- spavlick@mit.edu
        Jasmeet Arora     -- jasmeet@mit.edu
        Davis Tran        -- dvtran@mit.edu

Graduate Mentor----------------------------------------------------------------

        Will Boyd         -- wboyd@mit.edu

===============================================================================
                              REACTOR DESCRIPTION
===============================================================================

This benchmark is a 4x4 BWR reactor containing 14 fuel pins of 3 wt.% UO2 and 2
fuel pins of poisoned fuel containing 3 wt.% UO2 and 3 wt.% GD2O3. The fuel is 
contained in Zircaloy-2 clad. The moderator is water.

===============================================================================
                             NOTES ABOUT PLOTTING
===============================================================================

At the end of the code, plotting is commented out in order to prevent the code
from breaking if the user does not have matplotlib installed. Matplotlib is
a python module that can be installed using the following command:
    
    >$ sudo apt-get install python-matplotlib

===============================================================================
                                    SOURCES
===============================================================================

"MOCUM: A two-dimensional method of characteristics code based on constructive 
solid geometry and unstructured meshing for general geometries" is a research
article written by Xue Yang and Nader Satvat. It was published online on April 
9, 2012.
