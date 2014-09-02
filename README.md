arcus-sim-backend
=================

Code for extracting FITS spectra from a simulation of an Arcus X-ray spectrum.

=================

Arcus is a proposed X-ray grating spectrometer for the ISS.  This project will be python-based (more specifically largely astropy based) and will read the output of the simulator SIXTE (http://www.sternwarte.uni-erlangen.de/research/sixte/) when run for arcus and extract pha spectra.  The basic analysis steps were outlined by David Huenemoerder:

1) Assume that we have a "Level 1" event file, which minimally
  contains the columns:


 TIME, CCD_ID, CHIPX, CHIPY, ENERGY, DETX, DETY, X, Y,


 DETX and DETY will be some focal plane coordinate system which tiles
 the CCDs (useful for looking at the whole field).  X,Y will be some
 aspect-corrected coordinate system (for chandra this is a sky pixel,
 but that is not relevant here, except for zeroth order). [can we
 ignore aspect correction? that is, no dither, and we always have the
 same aim point (simulations)].


2) Define a region which contains the zeroth order, and determine it's
  centroid (in dither-corrected coordinates).


3) Define spatial regions (in X, Y) which will contain the dispersed
  spectrum for a given module.


4) For each event in the spectral region, transform coordinates (using
  the off-plane dispersion relation, zeroth order location, geometry,
  and aspect solution) to dispersion coordinates (essentially angles
  along dispersion and across).  Assign an m*lambda (order times
  wavelength) to each event.


  [We could probably do this in a fairly ad hoc way, by transforming
  the dispersion arc to a linear coordinate system, and not actually
  trying to locate the zeroth order or dispersed spectrum. So step 2
  is moot, and step 3 is pre-determined.]


5) Use the CCD ENERGY to compute a real-valued order for each event.
  That is, we know (m*lambda) ~ (m/E).


  We have an approximate E from the CCD ENERGY, so 


   m' = (m/E) * ENERGY.


   Add this real-valued estimate of the order to the event file, call
   it tg_m_real. (we eventually would like tg_m, the integer order).


6) Before we bin the events, we now need to filter appropriately.  We
  need to define a wavelength grid (low,high wavelength boundaries,
  per each order), a cross-dispersion width (which needn't be
  constant with wavelength, but for convenience a rectangle might be
  good enough), and order boundaries.  The order filter should come
  from the CCD response and be chosen, for instance, to give some
  large fraction of the response, say 95%.  So tg_m_real limits will
  in general be a function of energy. (For Chandra gratings, we
  tabulate in the CALDB the E_low( E ) and E_high( E ) and the
  enclosed fraction; here a rectangle might also be good enough.)


  Given these regions we can filter and bin into a standard PHA-type
  spectrum file.


7) In order to analyze the data, we need the responses, and these need
  to correspond to the filter and include detector geometry and
  aspect information.  For chandra gratings, the effective area is
  for a full spatial extraction aperture, but includes
  order-selection efficiency factor from the CCD response, and the
  detector geometry (chip gaps) and aspect solution (dither) for the
  efficiency vs wavelength.


  The grating response matrix (RMF) includes the aperture-selection
  information.  This is because in general the LSF and
  cross-dispersion efficiency do not factor --- if you change your
  spatial extraction width, you change the efficiency AND the
  profile.  Hence, they are strongly coupled, and we interpolate in
  tables stored in the CALDB.  The aperture efficiency factor is thus
  included in the RMF.
  
From Randy McEntaffer, the off-plane grating and LSF equations are:
The current LSF based on measured SPO data is a double Gaussian, f:

ax = exp(-0.5*((xdata-coeffs[2])/coeffs[4])^2)
bx = exp(-0.5*((xdata-coeffs[3])/coeffs[5])^2)

f = coeffs[0]*ax+coeffs[1]*bx+coeffs[6]

with coeffs=[1.5594215e+008, 20923465., 178.65726, 179.69612, 2.4961202,
15.360183, 1000003.4]

with 24 micron pixels at 20 m this produces a central Gaussian with
1.45" FWHM and a broader Gaussian at 8.95" FWHM.   The broad Gaussian
contains 45% of the power.

I've only recently been successful in forcing my raytrace to produce
such a PSF in the telescope so I don't have an aberration function for
the gratings yet.  However, the dispersion equation is:

x(n,lambda) = n*lambda*2.87 (mm/ang)

So this gives you the x distance (in mm) from 0 order that you should
expect a given wavelength (in angstroms) and order (n).  To be clear, x
is the linear dispersion distance not a distance along the arc.

  
=================
  
With Arcus in practice the zero-order centroid will rarely be used directly for analyis as outlined above, since position
knowledge will need to be determed on the time scale of readouts (0.1 s) due to ISS motions.  The centroid of the fully accumulated (i.e., many ks of exposure) will be used as a check but for the most part the metrology system + star trackers should be giving us steps 2 and 3 above so we will be assuming that here.  Later we would like to add in the uncertainties in the positions of the zero-order and disperse spectrum.

Overview of code structure
=================
The pyfits / astropy.io.fits package can read in the events list in a dictionary object.  The x,y columns will initially be simply in the dispersion and cross-dispersion directions.  


