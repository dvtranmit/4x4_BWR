from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize

#still not sure what this does. tough concept.
materials = materialize.materialize('BWR_materials.hdf5')

#finds the identification number for each material
uo2_id = matrials['UO2'].gedId()
moderator_id = materials['MODERATOR'].gedId()
clad_id = materials['CLAD'].gedId()

#printing materials for reference while coding and debugging
print materials
print len(materials)

#creates list of circle and plane surfaces
circles = [] 
planes = []

#appends surfaces to lists
planes.append(XPlane(x=-0.8))
planes.append(XPlane(x=0.8))
planes.append(YPlane(y=-0.8))
planes.append(YPlane(y=0.8))
circles.append(Circle(x=0.0, y=0.0, radius=0.6))
circles.append(Circle(x=0.0, y=0.0, radius=0.5))

#sets the boundary type for the planes to be reflective (neutrons bounce back)
for plane in planes:plane.setBoundaryType(REFLECTIVE)

log.py_printf("Normal", "Creating cells...")

#creates cells that contain materials (square, ring, circle cells)
cells = []
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=clad_id))
cells.append(CellBasic(universe=1, material=moderator_id))

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
