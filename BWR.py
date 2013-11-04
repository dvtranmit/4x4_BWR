from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize

materials = materialize.materialize('BWR_materials.hdf5')
print materials
print len(materials)
