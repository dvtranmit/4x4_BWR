from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize

materials = materialize.materialize('BWR_materials.hdf5')
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

