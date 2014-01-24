from openmoc import *
import openmoc.plotter as plotter
import openmoc.log as log
import openmoc.process as process
import h5py

def createCells(uo2_id, water_id, circle, left, right, bottom, top):

    log.py_printf('NORMAL', 'Creating cells...')

    cells = []
    cells.append(CellBasic(universe=1, material=uo2_id))
    cells.append(CellBasic(universe=1, material=water_id))
    cells.append(CellFill(universe=0, universe_fill=2))

    cells[0].addSurface(halfspace=-1, surface=circle)
    cells[1].addSurface(halfspace=+1, surface=circle)
    cells[2].addSurface(halfspace=+1, surface=left)
    cells[2].addSurface(halfspace=-1, surface=right)
    cells[2].addSurface(halfspace=+1, surface=bottom)
    cells[2].addSurface(halfspace=-1, surface=top)

    return cells

def createLattice():

    log.py_printf('NORMAL', 'Creating simple pin cell lattice...')

    lattice = Lattice(id=2, width_x=4.0, width_y=4.0)
    lattice.setLatticeCells([[1]])
    
    return lattice


def createGeometry(materials, cells, lattice):
    
    log.py_printf('NORMAL', 'Creating geometry...')

    geometry = Geometry()
    for material in materials.values(): geometry.addMaterial(material)
    for cell in cells: geometry.addCell(cell)
    geometry.addLattice(lattice)

    geometry.initializeFlatSourceRegions()
    
    return geometry

def createTrackGen(geometry, num_azim, track_spacing):

    log.py_printf('NORMAL', 'Initializing the track generator...')

    track_generator = TrackGenerator(geometry, num_azim, track_spacing)
    track_generator.generateTracks()

    return track_generator

def createSolver(geometry, track_generator, num_threads, tolerance, max_iters):

    solver = ThreadPrivateSolver(geometry, track_generator)
    solver.setNumThreads(num_threads)
    solver.setSourceConvergenceThreshold(tolerance)
    solver.convergeSource(max_iters)
    solver.printTimerReport()

