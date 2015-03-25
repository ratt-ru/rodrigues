# Layout of a Simulation container

version: 0.2

## introduction

This page describes the layout of a simulation container.


## requirements

* Entrypoint of the container should be a script in the root wit the name
  `/run.sh`.
* The scripts should accept one argument, a directory where it can find the
  input and output folder (default /)
* The simulation can accept parameters which can be defined by a file
  `/input/parameters.json` which will be bound into the container at runtime.
* The paramaters file is a json file, which contain nested structures. The root
  structure should be a
  dictionary/mapping where the key is the parameter to set and the value.
* Simulator Dockerfile should be in public repository and buildable without
  intervention.
* All logging should go to STDOUT and STDERR.




## commands:
Example command to run the split IO simulator:
```
docker run \
    -v <input_folder>/input:ro \
    -v <output_folder>/output:rw \
    <container_name>
    /run.sh
```

##parameters.json example

```
{
   "casa_niter":1000,
   "lwimager_cyclefactor":1.5,
   "wsclean_beamsize":"",
   "casa_restoringbeam":"",
   "vis_noise_std":0.0,
   "casa_cyclefactor":1.5,
   "observatory":"MK",
   "wsclean":false,
   "lwimager_niter":1000,
   "ms_freq0":700.0,
   "sefd":null,
   "im_mode":"C",
   "lwimager":false,
   "moresane_edgesupression":false,
   "lwimager_operation":"C",
   "name":"New simulation",
   "wsclean_sigmalevel":0.0,
   "moresane_stopscale":20,
   "output":"I",
   "ms_dfreq":50000.0,
   "wsclean_cleanborder":5.0,
   "ms_dec":"-30d0m0s",
   "im_wprojplanes":0,
   "im_stokes":"I",
   "moresane_edgeoffset":0,
   "radius":0.5,
   "imager":"LW",
   "casa_threshold":0.0,
   "casa_gridmode":"W",
   "ms_synthesis":0.25,
   "im_weight":"N",
   "lwimager_sigmalevel":0.0,
   "im_weight_fov":null,
   "lwimager_stoppointmode":-1.0,
   "wsclean_mgain":0.1,
   "wsclean_multiscale_dash_scale_dash_bias":0.6,
   "moresane_subregion":null,
   "wsclean_nonegative":false,
   "katalog_id":"NV",
   "casa_cyclespeedup":-1.0,
   "wsclean_multiscale_dash_threshold_dash_bias":0.7,
   "moresane":false,
   "casa_imagermode":"C",
   "moresane_loopgain":0.1,
   "fluxrange":"0.001-1",
   "moresane_tolerance":0.75,
   "moresane_startscale":1,
   "lwimager_gain":0.1,
   "wsclean_smallpsf":false,
   "wsclean_niter":1000,
   "lwimager_uservector":"",
   "casa_reffreq":null,
   "add_noise":true,
   "lwimager_cyclespeedup":-1.0,
   "casa_smallscalebias":0.6,
   "lwimager_nscales":4,
   "casa_psfmode":"CL",
   "im_npix":512,
   "ms_dtime":10,
   "moresane_mfs":false,
   "ms_nchan":1,
   "casa":false,
   "moresane_minorloopmiter":50,
   "channelise":0,
   "moresane_accuracy":1e-06,
   "moresane_convmode":"C",
   "wsclean_stopnegative":false,
   "moresane_majorloopmiter":100,
   "sky_type":"T",
   "casa_multiscale":"",
   "ms_ra":"0h0m0s",
   "wsclean_joinpolarizations":false,
   "ms_start_time":-0.125,
   "im_robust":0.0,
   "im_cellsize":1.0,
   "moresane_enforcepositivity":false,
   "wsclean_joinchannels":false,
   "ms_scan_length":0.25,
   "casa_gain":0.1,
   "sky_model":null,
   "casa_sigmalevel":0.0,
   "moresane_sigmalevel":3.0,
   "moresane_spi_dash_sigmalevel":10.0,
   "wsclean_multiscale":false,
   "casa_nterms":1,
   "wsclean_gain":0.1,
   "lwimager_threshold":0.0,
   "wsclean_threshold":0.0,
   "moresane_scalecount":null,
   "casa_negcomponent":-1.0
}
```
