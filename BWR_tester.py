from openmoc import *
import openmoc.plotter as plotter
import openmoc.log as log
import openmoc.process as process
import h5py

def createCells(r, s, circles, planes, uo2_id, clad_id, moderator_id, gd2o3_id):

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

    #third cell
    cells[2].addSurface(halfspace=+1, surface=circles[0])

    ## Fuel Type: UO2 + GD2O3: Universe=2 ##


    #fourth cell, region within small circle
    cells[3].addSurface(halfspace=-1, surface=circles[1])

    #fifth cell, region inside big and outside small circle
    cells[4].addSurface(halfspace=-1, surface=circles[0])
    cells[4].addSurface(halfspace=+1, surface=circles[1])

    #sixth cell, region outside the big circle; the square formed by the four planes
    cells[5].addSurface(halfspace=+1, surface=circles[0])

    #seventh cell, giant cell
    #this takes care of the big square surrounding the entire system
    cells[6].addSurface(halfspace=+1, surface=planes[0])
    cells[6].addSurface(halfspace=+1, surface=planes[2])
    cells[6].addSurface(halfspace=-1, surface=planes[1])
    cells[6].addSurface(halfspace=-1, surface=planes[3])

    return cells

def createLattice():

    log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')

    lattice = Lattice(id=3, width_x=1.6, width_y=1.6)

    lattice.setLatticeCells([[1, 1, 1, 1],
                             [1, 2, 1, 1],
                             [1, 1, 2, 1],
                             [1, 1, 1, 1]])
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

def createSolver(geometry, track_generator, num_threads, tolerance, max_iters, k_fsr):

    solver = ThreadPrivateSolver(geometry, track_generator)
    solver.setNumThreads(num_threads)
    solver.setSourceConvergenceThreshold(tolerance)
    solver.convergeSource(max_iters)
    solver.printTimerReport()

