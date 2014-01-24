from openmoc import * 
import openmoc.log as log # this module stores data printed during simulation
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import openmoc.process as process
import h5py
import numpy as np
from BWR_tester import *
from openmoc.options import Options

options = Options()

###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

num_threads = options.num_omp_threads
track_spacing = options.track_spacing
num_azim = options.num_azim
tolerance = options.tolerance
max_iters = options.max_iters

log.setLogLevel('DEBUG')

###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('BWR_materials.hdf5')

uo2_id = materials['UO2'].getId()
moderator_id = materials['MODERATOR'].getId()
clad_id = materials['CLAD'].getId()
gd2o3_id = materials['UO2 + GD2O3'].getId() 


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating Surfaces...')

#creates list of circle and plane surfaces
circles = [] 
planes = []

#appends surfaces to listsg
planes.append(XPlane(x=-3.2))
planes.append(XPlane(x=3.2))
planes.append(YPlane(y=-3.2))
planes.append(YPlane(y=3.2))
circles.append(Circle(x=0.0, y=0.0, radius=0.6))
circles.append(Circle(x=0.0, y=0.0, radius=0.5))

#sets the boundary type for the planes to be reflective (neutrons bounce back)
for plane in planes:plane.setBoundaryType(REFLECTIVE)



r = 3
s = 8
k_fsr = []

num_azims = [4,8,16]
k_angles = []
track_spacing = 0.1
counter = 0
geometries = []
cells_dict = {}
lattices = {}


cells = createCells(r, s, circles, planes, uo2_id, clad_id, moderator_id, gd2o3_id)
cells_dict['%s' % (str(counter))] = cells
lattice = createLattice()
lattices['%s' % (str(counter))] = lattice
geometry = createGeometry(materials, cells, lattice)
geometries.append(geometry)
track_generator = createTrackGen(geometries[counter], num_azim, track_spacing)
k_angle = createSolver(geometries[counter], track_generator, num_threads, tolerance, max_iters, k_fsr)
k_angles.append(k_angle)
counter += 1

'''print k_angles

#Resets cells to default FSR values for the other two tables
cells = []
cells.append(CellBasic(universe=1, material=uo2_id, rings=3, sectors=16))
cells.append(CellBasic(universe=1, material=clad_id, sectors=16))
cells.append(CellBasic(universe=1, material=moderator_id, sectors=16))
cells.append(CellBasic(universe=2, material=gd2o3_id, rings=3, sectors=16)) 
cells.append(CellBasic(universe=2, material=clad_id, sectors=16))
cells.append(CellBasic(universe=2, material=moderator_id, sectors=16))

k_az = []
k_ts = []


az_values = [4, 8, 16, 32, 64, 128, 256]
ts_values = [0.5, 0.1, 0.05, 0.01]
maxpin_az = np.zeros(len(az_values))
avgpin_az = np.zeros(len(az_values))
maxpin_ts = np.zeros(len(ts_values))
avgpin_ts = np.zeros(len(ts_values))


def computeMaxAndAvgPinPowers(solver, geometry):
    process.computeFSRPinPowers(solver, geometry, use_hdf5=True)
#    return 0, 0
    actualPinPowers = np.array([[1, 2, 3, 4], 
                               [5, 6, 7, 8], 
                               [9, 10, 11, 12], 
                               [13, 14, 15, 16]])
        
    f = h5py.File('pin-powers/fission-rates.hdf5', 'r') 
    calculatedPinPowers = f['universe0']['fission-rates'][...]
    normalizedPinPowers = calculatedPinPowers/np.sum(calculatedPinPowers)
    pinError = (normalizedPinPowers - actualPinPowers) / actualPinPowers
    f.close()
    return np.max(pinError), np.mean(pinError)

for index, num_azim in enumerate(az_values):

    log.py_printf('NORMAL', 'Initializing the track generator...')

    #Creates an instance of the TrackGenerator class, takes three parameters
    track_generator =TrackGenerator(geometry, num_azim, 0.1) #track_spacing
    #Runs the generateTracks() method of the TrackGenerator class
    track_generator.generateTracks()

    ###############################################################################
    #########################   Running a Simulation ##############################
    ###############################################################################

    #Creates an instance of the ThreadPrivateSolver class with two parameters
    solver = ThreadPrivateSolver(geometry, track_generator)
    #Sets the number of threads with the number imported from options
    solver.setNumThreads(num_threads)
    #sets the convergence threshold with tolerance imported from options
    solver.setSourceConvergenceThreshold(tolerance)
    #This is where the simulation is actually run. max_iters here is the 
    #number of iterations for the simulation.
    solver.convergeSource(max_iters)
    #Prints a report with time elapsed 
    solver.printTimerReport()

    maxpin_az[index], avgpin_az[index] = computeMaxAndAvgPinPowers(solver, geometry)
    
        
    k_az.append(solver.getKeff())


for index, track_spacing in enumerate(ts_values):

    log.py_printf('NORMAL', 'Initializing the track generator...')

    #Creates an instance of the TrackGenerator class, takes three parameters
    track_generator = TrackGenerator(geometry, 128, track_spacing) #num_azim
    #Runs the generateTracks() method of the TrackGenerator class
    track_generator.generateTracks()

    ###############################################################################
    #########################   Running a Simulation ##############################
    ###############################################################################

    #Creates an instance of the ThreadPrivateSolver class with two parameters
    solver = ThreadPrivateSolver(geometry, track_generator)
    #Sets the number of threads with the number imported from options
    solver.setNumThreads(num_threads)
    #sets the convergence threshold with tolerance imported from options
    solver.setSourceConvergenceThreshold(tolerance)
    #This is where the simulation is actually run. max_iters here is the 
    #number of iterations for the simulation.
    solver.convergeSource(max_iters)
    #Prints a report with time elapsed 
    solver.printTimerReport()

    maxpin_ts[index], avgpin_ts[index] = computeMaxAndAvgPinPowers(solver, geometry)
  
    k_ts.append(solver.getKeff())'''

'''counter = 0
for keff in k_az:   
    log.py_printf('NORMAL', 'num_azim = ' + str(az_values[counter]) + ' k-eff = ' + str(keff))
    log.py_printf('NORMAL', 'deltaK = ' + str(keff - 0.986561))
    log.py_printf('NORMAL', ' ')
    counter += 1

counter = 0
for keff in k_ts:    
    log.py_printf('NORMAL', 'track_spacing = ' + str(ts_values[counter]) + ' k-eff = ' + str(keff))
    log.py_printf('NORMAL', 'deltaK = ' + str(keff - 0.986561))
    log.py_printf('NORMAL', ' ')
    counter += 1

counterR = 0
counterS = 0
for keff in k_fsr:  
    if counterS > 3:                
        counterR += 1
        counterS = 0
        log.py_printf('NORMAL', 'rings = ' + str(ring_values[counterR]) + ' sectors = ' + str(sector_values[counterS]) + ' k-eff = ' + str(keff))
        log.py_printf('NORMAL', 'deltaK = ' + str(keff - 0.986561))
        log.py_printf('NORMAL', ' ')
        counterS += 1  
    else:
        log.py_printf('NORMAL', 'rings = ' + str(ring_values[counterR]) + ' sectors = ' + str(sector_values[counterS]) + ' k-eff = ' + str(keff))
        log.py_printf('NORMAL', 'deltaK = ' + str(keff - 0.986561))
        log.py_printf('NORMAL', ' ')
        counterS +=1'''
'''            
###############################################################################
############################   Generating Plots   #############################
###############################################################################'''


"""log.py_printf('NORMAL', 'Plotting data...')

#Plots the tracks generated by TrackGenerator using MatPlotLib
plotter.plotTracks(track_generator)
#Figures out the line segments based on the track intersections
plotter.plotSegments(track_generator)
#Color codes the segments by material
plotter.plotMaterials(geometry, gridsize=500)
#Separates the tracks into cells
plotter.plotCells(geometry, gridsize=500)
#Plots the flat source regions with different colors
plotter.plotFlatSourceRegions(geometry, gridsize=500)
#Plots flow of neutrons out of a given area...with color!
#We have two energy groups, so the array has two values.
plotter.plotFluxes(geometry, solver, energy_groups=[1,2])

#prints finished status for the plot generator
log.py_printf('TITLE', 'Finished')"""
