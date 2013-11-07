from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize

###############################################################################
###########################   Creating Materials   ############################
###############################################################################

#still not sure what this does. tough concept.
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


