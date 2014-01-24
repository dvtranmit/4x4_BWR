from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options
from pincelltester import *


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.num_omp_threads
track_spacing = options.track_spacing
num_azim = options.num_azim
tolerance = options.tolerance
max_iters = options.max_iters

log.setLogLevel('NORMAL')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('../c5g7-materials.h5')

uo2_id = materials['UO2'].getId()
water_id = materials['Water'].getId()


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circle = Circle(x=0.0, y=0.0, radius=1.0)
left = XPlane(x=-2.0)
right = XPlane(x=2.0)
top = YPlane(y=2.0)
bottom = YPlane(y=-2.0)

left.setBoundaryType(REFLECTIVE)
right.setBoundaryType(REFLECTIVE)
top.setBoundaryType(REFLECTIVE)
bottom.setBoundaryType(REFLECTIVE)



cells = createCells(uo2_id, water_id, circle, left, right, bottom, top)
lattice = createLattice()
geometry = createGeometry(materials, cells, lattice)
track_generator = createTrackGen(geometry, num_azim, track_spacing)
createSolver(geometry, track_generator, num_threads, tolerance, max_iters)



###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

#plotter.plotTracks(track_generator)
#plotter.plotSegments(track_generator)
#plotter.plotMaterials(geometry, gridsize=500)
#plotter.plotCells(geometry, gridsize=500)
#plotter.plotFlatSourceRegions(geometry, gridsize=500)
#plotter.plotFluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')
