from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize

materials = materialize.materialize('BWR_materials.hdf5')

uo2_id = matrials['UO2'].gedId()
moderator_id = materials['MODERATOR'].gedId()
clad_id = materials['CLAD'].gedId()

print materials
print len(materials)

circles = [] 
planes = []

planes.append(XPlane(x=-0.8))
planes.append(XPlane(x=0.8))
planes.append(YPlane(y=-0.8))
planes.append(YPlane(y=0.8))
circles.append(Circle(x=0.0, y=0.0, radius=0.6))
circles.append(Circle(x=0.0, y=0.0, radius=0.5))
for plane in planes:plane.setBoundaryType(REFLECTIVE)

log.py_printf("Normal", "Creating cells...")

cells = []
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=clad_id))
cells.append(CellBasic(universe=1, material=moderator_id))

cells[0].addSurface(halfspace=-1, surface=circles[1])

cells[1].addSurface(halfspace=-1, surface=circles[0])
cells[1].addSurface(halfspace=+1, surface=circles[1])

cells[2].addSurface(halfspace=+1, surface=planes[0])
cells[2].addSurface(halfspace=+1, surface=planes[2])
cells[2].addSurface(halfspace=-1, surface=planes[1])
cells[2].addSurface(halfspace=-1, surface=planes[3])
cells[2].addSurface(halfspace=+1, surface=circles[0])
