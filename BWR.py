"""Imports all modules from OpenMOC, as well as the individual functions log, 
plotter, and materialize, all of which are part of submodules within OpenMoc"""

from openmoc import * 
import openmoc.log as log # this module stores data printed during simulation
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import openmoc.process as process
import h5py
import numpy as np

###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

"""This imports a variety of variables from the options file. This should be 
located within the OpenMOC folder.This could potentially also accept user input,
but there should also be a default value."""

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

#The following assigns the dictionary returned by the materialize function in 
#the materialize python file to the variable materials
materials = materialize.materialize('BWR_materials.hdf5')

#finds the identification number for each material
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


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

#Code currently changes FSR to test delta k

ring_values = [2, 3, 4, 5]
sector_values = [2, 4, 8, 16]
k_fsr = []

for r in ring_values:
    for s in sector_values:

        log.py_printf("Normal", "Creating cells...")

        #creates cells that contain materials (square, ring, circle cells)
        cells = []
        cells.append(CellBasic(universe=1, material=uo2_id, rings=r, sectors=s))
        cells.append(CellBasic(universe=1, material=clad_id, sectors=s))
        cells.append(CellBasic(universe=1, material=moderator_id, sectors=s))
        cells.append(CellBasic(universe=2, material=gd2o3_id, rings=r, sectors=s)) 
        cells.append(CellBasic(universe=2, material=clad_id, sectors=s))
        cells.append(CellBasic(universe=2, material=moderator_id, sectors=s))

        #creates cells that are filled by the lattice universe
        cells.append(CellFill(universe=0, universe_fill=3))

        ## Fuel Type: UO2: Universe=1 ##

        #first cell, region within small circle
        cells[0].addSurface(halfspace=-1, surface=circles[1])

        #second cell, region inside big and outside small circle
        cells[1].addSurface(halfspace=-1, surface=circles[0])
        cells[1].addSurface(halfspace=+1, surface=circles[1])

        #third cell, region outside the big circle; the square formed by the four planes 
        #will be taken care of with the lattice
        #cells[2].addSurface(halfspace=+1, surface=planes[0])
        #cells[2].addSurface(halfspace=+1, surface=planes[2])
        #cells[2].addSurface(halfspace=-1, surface=planes[1])
        #cells[2].addSurface(halfspace=-1, surface=planes[3])
        cells[2].addSurface(halfspace=+1, surface=circles[0])



        ## Fuel Type: UO2 + GD2O3: Universe=2 ##


        #fourth cell, region within small circle
        cells[3].addSurface(halfspace=-1, surface=circles[1])

        #fifth cell, region inside big and outside small circle
        cells[4].addSurface(halfspace=-1, surface=circles[0])
        cells[4].addSurface(halfspace=+1, surface=circles[1])

        #sixth cell, region outside the big circle; the square formed by the four planes
        #will be taken care of with the lattice

        #cells[5].addSurface(halfspace=+1, surface=planes[0])
        #cells[5].addSurface(halfspace=+1, surface=planes[2])
        #cells[5].addSurface(halfspace=-1, surface=planes[1])
        #cells[5].addSurface(halfspace=-1, surface=planes[3])
        cells[5].addSurface(halfspace=+1, surface=circles[0])

        #seventh cell, giant cell
        #this takes care of the big square surrounding the entire system
        cells[6].addSurface(halfspace=+1, surface=planes[0])
        cells[6].addSurface(halfspace=+1, surface=planes[2])
        cells[6].addSurface(halfspace=-1, surface=planes[1])
        cells[6].addSurface(halfspace=-1, surface=planes[3])

        ###############################################################################
        ###########################   Creating Lattices   #############################
        ###############################################################################

        log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')

        """A universe is a space containing a fuel pin within our 4x4 lattice. Further 
        comments below on how the lattice was created."""

        lattice = Lattice(id=3, width_x=1.6, width_y=1.6)
        """This lattice can be considered our third universe, 1 and 2 being the UO2 and 
        gd2o3 fuel pins respectively. This is why lattice has an ID of 3. Width 
        and Height of each little square are taken from the diagram provided with the 
        data."""

        lattice.setLatticeCells([[1, 1, 1, 1],
                                 [1, 2, 1, 1],
                                 [1, 1, 2, 1],
                                 [1, 1, 1, 1]])

        """Each 1 represents a UO2 fuel pin cell, and each 2 represents a gd2o3 fuel pin 
        cell in our lattice."""

        ###############################################################################
        ##########################   Creating the Geometry   ##########################
        ###############################################################################

        log.py_printf('NORMAL', 'Creating geometry...')

        geometry = Geometry() 
        """Creates an instance of the Geometry class. This is a 
        class in the openmoc file."""

        for material in materials.values(): geometry.addMaterial(material)
        """This one line has a long explanation. Earlier in this file, we ran our
        materials data through the materialize function and assigned that dictionary
        to the variable "materials". That means "materials" is a dictionary containing
        each material as the key, and its attributes (sigma_a, sigma_s, etc...) as 
        values. The .values() operator returns a list of all the values in the 
        materials dictionary. The for loop loops through each material in the list
        and adds that material to the geometry. One confusing thing here is that
        after the colon, the block of code isn't indented below the for loop--it 
        continues on the same line. It would function the same if it were written
        like this:

        for material in materials.values():
            geometry.addMaterial(material)

        """

        for cell in cells: geometry.addCell(cell)
        """Same deal here, except cells is a list of our cell types (we have 6). The
        for loop runs through the cell list and adds each cell to the geometry 
        (which is, once again, an instance of the Geometry class). The geometry class
        now understands what each universe in the lattice means so that adding
        the lattice in the next line makes sense to the geometry."""

        geometry.addLattice(lattice)
        """Adds the lattice we just created to the geometry."""

        geometry.initializeFlatSourceRegions()
        """Once the geometry attributes are set up, this method returns
        "_openmoc.Geometry_initializeFlatSourceRegions(self)" This figures out what each
        flat source region is in the geometry and gives each one a unique ID"""

        ###############################################################################
        ########################   Creating the TrackGenerator   ######################
        ###############################################################################

        #The following runs the simulation for changes in FSR

        log.py_printf('NORMAL', 'Initializing the track generator...')

        #Creates an instance of the TrackGenerator class, takes three parameters
        track_generator = TrackGenerator(geometry, num_azim, track_spacing)
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
        
        k_fsr.append(solver.getKeff())


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
  
    k_ts.append(solver.getKeff())

counter = 0
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
        counterS +=1          
            
###############################################################################
############################   Generating Plots   #############################
###############################################################################


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
