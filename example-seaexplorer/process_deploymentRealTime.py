import logging
import os
import pyglider.seaexplorer as seaexplorer
import pyglider.ncprocess as ncprocess
import pyglider.plotting as pgplot

logging.basicConfig(level='INFO')

sourcedir = '~alseamar/Documents/SEA035/000012/000012/C-Csv/*'
rawdir  = './realtime_raw/'
rawncdir     = './realtime_rawnc/'
deploymentyaml = './deploymentRealtime.yml'
l0tsdir    = './L0-timeseries/'
profiledir = './L0-profiles/'
griddir    = './L0-gridfiles/'
plottingyaml = './plottingconfig.yml'

# get the data from where it is pushed by Alseamar.  Contact them to set this
# up...
if False:
    os.system('rsync -av ' + sourcedir + ' ' + rawdir)

# clean last processing...
os.system('rm ' + rawncdir + '* ' + l0tsdir + '* ' + profiledir + '* ' +
          griddir + '* ')

# turn *.EBD and *.DBD into *.ebd.nc and *.dbd.nc netcdf files:
seaexplorer.raw_to_rawnc(rawdir, rawncdir, deploymentyaml)

# merge individual netcdf files into single netcdf files *.ebd.nc and *.dbd.nc:
seaexplorer.merge_rawnc(rawncdir, rawncdir, deploymentyaml, kind='sub')

# Make timeseries netcdf file from th raw files:
outname = seaexplorer.raw_to_timeseries(rawncdir, l0tsdir, deploymentyaml, kind='sub')

# write time series as a collection of individual profiles:
ncprocess.extract_timeseries_profiles(outname, profiledir, deploymentyaml)

# make depth-profile grid
gridname = ncprocess.make_gridfiles(outname, griddir, deploymentyaml)

pgplot.grid_plots(grid, plottingyaml)
