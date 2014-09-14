"""
Main code for analysis of simulated arcus spectra

caldb class stores "CALDB" data:
CALDB consists of positions of CCDs in sky coordinates
positions of zero-orders in sky coordinates
center of dispersed spectrum in sky cooridnates
PSF model parameters and/or image
gratings equation coefficients
order "branching ratios"
detector QE

gr_events class
class to read in gratings events data
assumes minimum set of columns time, x, y, pha
since don't have an astropy based events class, makes sense to create one

arcus_sim class:
has caldb as data
has events as data
main fns.
__init__: read in caldb, events
fakeit(E, spec, exptime, bgdperpix=0.): quick-and-dirty generate fake events data, bgd in counts/pixel/s
fakeit_img(E, spec, exptime, E0=None, E1=None, order=None, bgdperpix=0.): as above but only makes image (e.g., no time or pha generation), bgd in counts/pixel
which_mod(x, y): returns which model the spectrum at x,y most likely corresponds to

extract_spectrum(x0, x1, y0, y1):

"""

