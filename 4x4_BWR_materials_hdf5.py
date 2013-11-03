import h5py
import numpy

#Import OS module
import os
#Removes previously created .hdf5 file from previous time code was run
os.system('rm BWR_materials.hdf5')

f = h5py.File('BWR_materials.hdf5') #opens the actual hdf5 file, note: the current
                                    #python file will take the data values and
                                    #store them in that hdf5 file. This is not
                                    #the hdf5 file itself.
f.attrs["Energy Groups"] = 4        #I think this is 4 for the number of materials

######################################################################
################################ UO2 #################################
######################################################################

uo2 = f.create_group('UO2')  #That's the letter 'O' not the number

#Entering data values for both groups of each material separated by a comma

sigma_t = numpy.array([3.62022e1, 5.72155e-1]) 
                                        
sigma_f = numpy.array([7.22964e-3, 1.41126e-1])

v_sigma_f = numpy.array([1.86278e-2, 3.44137e-1])

sigma_a = numpy.array ([2.76091e-2, 1.91257e-1])

sigma_s = numpy.array([3.33748e-1, 0.0, 6.64881e-4, 3.80898e-1])

chi = numpy.array([0.0,1.0])

#Creates data sets for each cross section type using the uo2 material

uo2.create_dataset('Total XS', data=sigma_t)
uo2.create_dataset('Absorption XS', data=sigma_a)
uo2.create_dataset('Fission XS', data=sigma_f)
uo2.create_dataset('Nu Fission XS', data=v_sigma_f)
uo2.create_dataset('Scattering XS', data=sigma_s)
uo2.create_dataset('Chi', data=chi)

######################################################################
########################## UO2 + GD2O3 ###############################
######################################################################

gd2o3 = f.create_group('UO2 + GD2O3')

#Entering data values for the UO2 + GD2O3 material

sigma_t = numpy.array([3.71785e-1, 1.75000e0])

sigma_f = numpy.array([6.97904e-3, 6.45724e-2])

sigma_a = numpy.array([3.29962e-2, 1.36680e0])

v_sigma_f = numpy.array([1.79336e-2, 1.57929e-1])

sigma_s = numpy.array([3.38096e-1, 0.0, 6.92807e-4, 3.83204e-1])

chi = numpy.array([0.0,1.0])

#Creates data sets for each cross section type for UO2 + GD2O3

gd2o3.create_dataset('Total XS', data=sigma_t)
gd2o3.create_dataset('Absorption XS', data=sigma_a)
gd2o3.create_dataset('Fission XS', data=sigma_f)
gd2o3.create_dataset('Nu Fission XS', data=v_sigma_f)
gd2o3.create_dataset('Scattering XS', data=sigma_s)
gd2o3.create_dataset('Chi', data=chi)

######################################################################
############################ Clad ####################################
######################################################################

clad = f.create_group('CLAD')

#Adds values for the clad subgroup

sigma_t = numpy.array([2.74144e-1, 2.80890e-1])

sigma_f = numpy.zeros(2)

sigma_a = numpy.array([1.57616e-3, 3.6600e-3])

v_sigma_f = numpy.zeros(2)

sigma_s = numpy.array([2.72377e-1,0.0, 1.90838e-4,2.77230e-1])

chi = numpy.array([0.0,0.0])

#Creates data sets for each cross section type for the clad material

clad.create_dataset('Total XS', data=sigma_t)
clad.create_dataset('Absorption XS', data=sigma_a)
clad.create_dataset('Fission XS', data=sigma_f)
clad.create_dataset('Nu Fission XS', data=v_sigma_f)
clad.create_dataset('Scattering XS', data=sigma_s)
clad.create_dataset('Chi', data=chi)

######################################################################
############################ Moderator ###############################
######################################################################

moderator = f.create_group('MODERATOR')

#Adds values for the moderator subgroup

sigma_t = numpy.array([6.40711e-1,1.69131])

sigma_f = numpy.zeros(2)

sigma_a = numpy.array([1.974e-4, 7.03e-3])

v_sigma_f = numpy.zeros(2)

sigma_s = numpy.array([6.07382e-1,0.0, 3.31316e-2,1.68428])

chi = numpy.array([0.0,0.0])

#Creates data sets for each cross section type

moderator.create_dataset('Total XS', data=sigma_t)
moderator.create_dataset('Absorption XS', data=sigma_a)
moderator.create_dataset('Fission XS', data=sigma_f)
moderator.create_dataset('Nu Fission XS', data=v_sigma_f)
moderator.create_dataset('Scattering XS', data=sigma_s)
moderator.create_dataset('Chi', data=chi)

f.close()
