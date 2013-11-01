import h5py
import numpy


"""I'm going to start entering data values into numpy arrays. Next step is to create a data group for each material, then create data sets within the data groups that contain the values I'm storing in each of the variables for each of the materials. Text me if that doesn't make sense. Final step is to write code that opens an hdf5 file, stores the data in the file, and closes the file. Remember not to run the code unless you're sure the file is closed because it might kill your memory. Ctrl D to stop the process! Also, I might be interpreting some of these steps wrong, so please correct me if I am!"""


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

sigma_t = numpy.array([3.62022*10^-1, 5.72155*10^-1]) 
                                        #I don't understand where all the numbers
                                        #are coming from in the example... doing my
                                        #best.
sigma_a = numpy.array([7.22964*10^-3, 1.41126*10^-1])

sigma_s = numpy.array([3.54792*10^-1, 4.31029*10^-1])

v_sigma_f = numpy.array([1.86278*10^-2, 3.44137*10^-1])

sigma_sg1 = numpy.array([3.33748*10^-1, 0.0])

sigma_sg2 = numpy.array([6.64881*10^-4, 3.80898*10^-1])

#Creates data sets for each cross section type using the uo2 material

uo2.create_dataset('Total XS', data=sigma_t)
uo2.create_dataset('Absorption XS', data=sigma_a)
uo2.create_dataset('Scattering XS', data=sigma_s)
uo2.create_dataset('Fission XS', data=v_sigma_f)
uo2.create_dataset('blank2', data=sigma_sg1)
uo2.create_dataset('blank3', data=sigma_sg2)

######################################################################
########################## UO2 + GD2O3 ###############################
######################################################################

gd2o3 = f.create_group('UO2 + GD2O3')

#Entering data values for the UO2 + GD2O3 material

sigma_t = numpy.array([3.71785*10^-1, 1.75000*10^0)]

sigma_a = numpy.array([6.97904*10^-3, 6.45724*10^-2)]

sigma_s = numpy.array([3.64806*10^-1,1.68525])

v_sigma_f = numpy.array([1.79336*10^-2, 1.57929*10^-1)]

sigma_sg1 = numpy.array([3.38096*10^-1, 0.0)]

sigma_sg2 = numpy.array([6.92807*10^-4, 3.83204*10^-1)]

#Creates data sets for each cross section type for UO2 + GD2O3

gd2o3.create_dataset('Total XS', data=sigma_t)
gd2o3.create_dataset('Absorption XS', data=sigma_a)
gd2o3.create_dataset('Scattering XS', data=sigma_s)
gd2o3.create_dataset('Fission XS', data=v_sigma_f)
gd2o3.create_dataset('blank2', data=sigma_sg1)
gd2o3.create_dataset('blank3', data=sigma_sg2)

######################################################################
############################ Clad ####################################
######################################################################

clad = f.create_group('CLAD')

#Adds values for the clad subgroup

sigma_t = numpy.array([2.74144*10^-1, 2.80890*10^-1])

sigma_a = numpy.zeros(2)

sigma_s = numpy.array([2.74144*10^-1, 2.80890*10^-1])

v_sigma_f = numpy.zeros(2)

sigma_sg1 = numpy.array([2.72377*10^-1,0.0])

sigma_sg2 = numpy.array([1.90838*10^-4,2.77230*10^-1])

#Creates data sets for each cross section type for the clad material

clad.create_dataset('Total XS', data=sigma_t)
clad.create_dataset('Absorption XS', data=sigma_a)
clad.create_dataset('Scattering XS', data=sigma_s)
clad.create_dataset('Fission XS', data=v_sigma_f)
clad.create_dataset('blank2', data=sigma_sg1)
clad.create_dataset('blank3', data=sigma_sg2)

######################################################################
############################ Moderator ###############################
######################################################################

moderator = f.create_group('MODERATOR')

#Adds values for the moderator subgroup

sigma_t = numpy.array([6.40711*10^-1,1.69131])

sigma_a = numpy.zeros(2)

sigma_s = numpy.array([6.40711*10^-1,1.69131])

v_sigma_f = numpy.zeros(2)

sigma_sg1 = numpy.array([6.07382*10^-1,0.0])

sigma_sg2 = numpy.array([3.31316*10^-2,1.68428])

#Creates data sets for each cross section type

moderator.create_dataset('Total XS', data=sigma_t)
moderator.create_dataset('Absorption XS', data=sigma_a)
moderator.create_dataset('Scattering XS', data=sigma_s)
moderator.create_dataset('Fission XS', data=v_sigma_f)
moderator.create_dataset('blank2', data=sigma_sg1)
moderator.create_dataset('blank3', data=sigma_sg2)

f.close()
