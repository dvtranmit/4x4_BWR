from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize

###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

"""This imports a variety of variables from the options file. This should be located within the OpenMOC folder.
This could potentially also accept user input, but there should also be a default value."""

num_threads = options.num_omp_threads
track_spacing = options.track_spacing
num_azim = options.num_azim
tolerance = options.tolerance
max_iters = options.max_iters

###############################################################################
###########################   Creating Materials   ############################
###############################################################################

#still not sure what this does. tough concept.
#Update: I think I get it. The following assigns the dictionary returned by the
#materialize function in the materialize python file to the variable materials
materials = materialize.materialize('BWR_materials.hdf5')

#finds the identification number for each material
uo2_id = materials['UO2'].gedId()
moderator_id = materials['MODERATOR'].gedId()
clad_id = materials['CLAD'].gedId()
gd2o3_id = materials['UO2 + GD2O3'].gedId() #added this material [12:54AM]

#printing materials for reference while coding and debugging
print materials
print len(materials)

###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

#creates list of circle and plane surfaces
circles = [] 
planes = []

#appends surfaces to listsg
planes.append(XPlane(x=-0.8))
planes.append(XPlane(x=0.8))
planes.append(YPlane(y=-0.8))
planes.append(YPlane(y=0.8))
circles.append(Circle(x=0.0, y=0.0, radius=0.6))
circles.append(Circle(x=0.0, y=0.0, radius=0.5))

#sets the boundary type for the planes to be reflective (neutrons bounce back)
for plane in planes:plane.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf("Normal", "Creating cells...")

#creates cells that contain materials (square, ring, circle cells)
cells = []
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=clad_id))
cells.append(CellBasic(universe=1, material=moderator_id))
cells.append(CellBasic(universe=2, material=gd2o3_id)) #new material
cells.append(CellBasic(universe=2, material=clad_id)) #same cladding
cells.append(CellBasic(universe=2, material=moderator_id)) #same moderator

## Fuel Type: UO2: Universe=1 ##

#first cell, region within small circle
cells[0].addSurface(halfspace=-1, surface=circles[1])

#second cell, region inside big and outside small circle
cells[1].addSurface(halfspace=-1, surface=circles[0])
cells[1].addSurface(halfspace=+1, surface=circles[1])

#third cell, region inside square formed by four planes and outside big circle
cells[2].addSurface(halfspace=+1, surface=planes[0])
cells[2].addSurface(halfspace=+1, surface=planes[2])
cells[2].addSurface(halfspace=-1, surface=planes[1])
cells[2].addSurface(halfspace=-1, surface=planes[3])
cells[2].addSurface(halfspace=+1, surface=circles[0])


## Fuel Type: UO2 + GD2O3: Universe=2 ##


#fourth cell, region within small circle
cells[3].addSurface(halfspace=-1, surface=circles[1])

#fifth cell, region inside big and outside small circle
cells[4].addSurface(halfspace=-1, surface=circles[0])
cells[4].addSurface(halfspace=+1, surface=circles[1])

#sixth cell, region inside square formed by four planes and outside big circle
cells[5].addSurface(halfspace=+1, surface=planes[0])
cells[5].addSurface(halfspace=+1, surface=planes[2])
cells[5].addSurface(halfspace=-1, surface=planes[1])
cells[5].addSurface(halfspace=-1, surface=planes[3])
cells[5].addSurface(halfspace=+1, surface=circles[0])

###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')

"""From what I gather, a universe is a block containing a fuel pin within our 4x4 lattice. So far we've only coded a universe containing a moderator, cladding, and UO2. I'm going to go ahead and create a second universe containing the gd2o3 fuel pin. Further comments below on how I created the lattice."""

lattice = Lattice(id=1, width_x=1.0, width_y=1.0)
"""Created an instance of a lattice, which in our case is our 4x4 BWR. I gave it an arbitrary id because I don't know where the example id came from, and gave it width_x and width_y of 1.0 because those seem pretty standard."""

lattice.setLatticeCells([[1, 1, 1, 1],
                         [1, 2, 1, 1],
                         [1, 1, 2, 1],
                         [1, 1, 1, 1]])

"""Each 1 represents a UO2 fuel pin cell, and each 2 represents a gd2o3 fuel pin cell in our lattice."""

###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry() 
"""Creates an instance of the Geometry class. This is a 
class in the openmoc folder. I couldn't find a description of the definitions 
in this class in the file but you guys can read the definitions of this class
in the openmoc python file itself."""

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
"_openmoc.Geometry_initializeFlatSourceRegions(self)" ... I don't know what
that means but if I had to guess, I would say it takes our geometry, runs
it through the c++ version of openmoc and returns whatever that c++ operator 
does to our geometry. Again, this is just my best guess."""

###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

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
#We think this is where the simulation is actually run. max_iters here is the 
#number of iterations for the simulation.
solver.convergeSource(max_iters)
#Prints data for each iteration???
solver.printTimerReport()

###############################################################################
############################   Generating Plots   #############################
###############################################################################

#Prints status of the plot generation
log.py_printf('NORMAL', 'Plotting data...')

#Plots the tracks generated by TrackGenerator using MatPlotLib
plotter.plotTracks(track_generator)
#Plots the various segments onto the tracks... color codes?
plotter.plotSegments(track_generator)
#Color codes the segments by material
plotter.plotMaterials(geometry, gridsize=500)
#Separates the tracks into cells
plotter.plotCells(geometry, gridsize=500)
#NO CLUE
plotter.plotFlatSourceRegions(geometry, gridsize=500)
#Plots flow of neutrons out of a given area...with color!
#We have two energy groups, so the array has two values.
plotter.plotFluxes(geometry, solver, energy_groups=[1,2])

#prints finished status for the plot generator
log.py_printf('TITLE', 'Finished')



"""Questions"""

"""1. What is a lattice id?"""
"""2. Is a universe kind of like one of the fuel pin blocks?"""
"""3. Why are the widths 1.0?"""
"""4. What does the underscore mean in _openmoc?"""
