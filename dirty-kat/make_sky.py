#/usr/bin/env python
import numpy as np

def make_sky(name, sources, phase_centre=[0,0], intensity_range=[0,1], emaj_range=[0,5], emin_range=[0,5],
             pa_range=[0,360], ra_d_opts=[0,1], dec_d_opts=[0,1], only_point=False, only_gauss=False, num_point=0):
    """
    Create a .txt sky model.

    INPUTS:
    name:               Name for file.
    sources:            Number of sources to include.
    phase_centre:       Center point for source distribution.
    intensity_range:    Upper and lower values for intensity distribution.
    emaj_range:         Upper and lower values for gaussian semi-major axis.
    emin_range:         Upper and lower values for gaussian semi-minor axis.
    pa_range:           Upper and lower values for gaussian position angle.
    ra_d_opts:          Mean and standard deviation for right ascension.
    dec_d_opts:         Mean and standard deviation for declination.
    only_point:         Boolean which forces all sources to be points.
    only_gauss:         Boolean which forces all sources to be gaussian.
    num_point:          Number of point sources when sky contains a mixture.
    """

    # Layout and formatting.
    parameters=["name","ra_d","ra_m","dec_d","dec_m","i","emaj_s","emin_s","pa_d"]
    formatting = "#format:" + "".join(" "+str(j) for j in parameters) + "\n"

    model = open("{}.txt".format(name), "w")
    model.write(formatting)

    # Structure array.
    sky = np.zeros(sources, dtype = [(j,np.float32) for j in parameters])

    new_descr = sky.dtype.descr
    new_descr[0] = (new_descr[0][0], "|S8")
    new_dtype = np.dtype(new_descr)
    sky = sky.astype(new_dtype)

    # Check for options.
    if (only_point&only_gauss):
        print "Conflicting options. Assuming only point sources."
        only_gauss = False
    if only_gauss:
        print "All sources will be gaussian - ignoring # of points."
        num_point = 0
    if only_point:
        print "All sources will be points - ignoring # of points."
        num_point = sources

    # Check that sources add up.
    if num_point>sources:
        print "# of point sources > total # of sources: reducing"
        num_point = sources

    ra_random_adjust = np.random.normal(ra_d_opts[0],ra_d_opts[1],sources)
    dec_random_adjust = np.random.normal(dec_d_opts[0],dec_d_opts[1],sources)

    # Manufacture location, extent and intensity for sources.
    for i in range(sources):
        sky["name"][i] = "S{}".format(i+1)
        sky["ra_m"][i], sky["ra_d"][i] = \
            np.modf(phase_centre[0] + ra_random_adjust[i])
        sky["ra_m"][i] = sky["ra_m"][i]*60
        sky["dec_m"][i], sky["dec_d"][i] = \
            np.modf(phase_centre[1] + dec_random_adjust[i])
        sky["dec_m"][i] = abs(sky["dec_m"][i]*60)
        sky["i"][i] = intensity_range[0] + np.random.random(1)*(intensity_range[1]-intensity_range[0])
        if (only_point or (i<num_point)):
            continue
        sky["emaj_s"][i] = emaj_range[0] + np.random.random(1)*(emaj_range[1]-emaj_range[0])
        sky["emin_s"][i] = emin_range[0] + np.random.random(1)*(emin_range[1]-emin_range[0])
        if sky["emin_s"][i]>sky["emaj_s"][i]:
            sky["emaj_s"][i], sky["emin_s"][i] = sky["emin_s"][i], sky["emaj_s"][i]
        sky["pa_d"][i] = pa_range[0] + np.random.random(1)*(pa_range[1]-pa_range[0])

    # Format the structure array. Not elegant.
    sky = np.array2string(sky)
    old_chars = ["[","]","(",")",",","'","\n "," S"]
    new_chars = ["","","","","","","\n", "S"]

    for i in range(len(old_chars)):
        sky = sky.replace(old_chars[i], new_chars[i])

    # Finish up and save.
    model.write(sky)
    model.close

if __name__=="__main__":
    make_sky("sky_model_50", sources=50, phase_centre=[0,-30], num_point=38, ra_d_opts=[0,0.5], dec_d_opts=[0,0.5])
