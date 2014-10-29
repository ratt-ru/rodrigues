<html>
<body background="images/kat3.jpg">
<br>
<font color="white" size="4">
<h1 align="center">SKA SA</h1>

<h2 align="center">MeerKAT Simulations</h2>

<p align="center"> <img src="images/work.jpg" width="280" height="100" title="work in progress"/> </p>

<form method="post" align="center" action="process.php">

<br>

 <h2 align="center">Personal Details</h2>
  <table style="width:700px" align="center" border=1 bgcolor="grey">
    <tr>
      <td>Name (Optional)</td>
      <td><input type="text" name="username"></td>
    </tr>
    <tr>
      <td>E-Mail Address (Required)</td>
      <td><input type="e-mail" name="e-mail"></td>
    </tr>
  </table>

 
 <h2 align="center">Global Settings</h2>
  <table style="width:700px" align="center" border=1 bgcolor="grey">
    <tr>
      <td>Sky Type</td>
      <td>
	<select name="skytype">
	  <option value="tigger_lsm">Tigger LSM</option>
	  <option value="FITS">FITS</option>
	  <option value="siamese_model">Siamese Model</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Sky Model</td>
      <td><input type="file" name="skyname"></td>
    </tr>
    <tr>
      <td>Upload TDL?</td>
      <td>
        <select name="upload_tdl">
          <option value="True">YES</option>
          <option value="False">NO</option>
        </select>
      </td>

    </tr>
    <tr>
      <td align="center">TDL Configuration File</td>
      <td><input type="file" name="tdlconf"></td>
    </tr>
    <tr>
      <td>TDL Section</td>
      <td><input type="text" name="tdlsection"></td>
    </tr>
    <tr>
      <td>Make PSF?</td>
      <td>
        <select name="make_psf">
          <option value="False">NO</option>
          <option value="True">YES</option>
        </select>
      </td>

    </tr>
        <td>Add Noise?</td>
      <td>
        <select name="add_noise">
          <option value="True">YES</option>
          <option value="False">NO</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Noise Standard Deviation</td>
      <td>
        <input type="number" name="vis_noise_std">
      </td>
    </tr>
    <tr>
      <td>Output</td>
      <td>
        <select name="output">
          <option value="image">Image</option>
          <option value="visibilities">Visibilities</option>
        </select>
      </td>
    </tr>

  </table>


  <h2 align="center">Observation Setup</h2>
  <table style="width:700px" align="center" border=1 bgcolor="grey">
    <tr>
      <td>Synthesis Time</td>
      <td><input type="number" name="ms_hours"></td>
    </tr>
    <tr>
      <td>Integration Time</td>
      <td><input type="number" name="ms_dtime"></td>
    </tr>
    <tr>
      <td>Start Frequency</td>
      <td><input type="text" name="ms_freq0">Hz</td>
    </tr>   
    <tr>    
      <td>Channel Width</td>
      <td><input type="text" name="ms_dfreq">Hz</td>
    </tr>   
    <tr>    
      <td>Number of Frequency Channels per Band</td>
      <td><input type="number" name="ms_nchan"></td>
    </tr>   
    <tr>
      <td>Number of Frequency Bands</td>
      <td><input type="number" name="ms_nband"></td>
    </tr>
    <tr>
      <td>Do you want Autocorrelation in your data?</td>
      <td>
        <select name="ms_writeAutoCorr">
          <option value="True">YES</option>
          <option value="False">NO</option>
        </select>
      </td>
    </tr>
    </tr>
      <tr>
      <td>Declination</td>
      <td><input type="number" name="ms_dec"></td>
    </tr>
    <tr>
      <td>Right Ascension</td>
      <td><input type="number" name="ms_ra"></td>
    </tr>
  </table>


  <h2 align="center">Dish Settings</h2>
  <table style="width:700px" align="center" border=1 bgcolor="grey">
      <tr>
      <td>Amplitude Phase Gains</td>
      <td><input type="text" name="ds_amp_phase_gains"></td>
    </tr>
    <tr>
      <td>Parallactic Angle Rotation</td>
      <td>
       <select name="ds_parallactic_angle_rotation">
        <option value="True">YES</option>
        <option value="False">NO</option>
      </td>
    </tr>
    <tr>
      <td>Primary Beam</td>
      <td>
        <select name="ds_primary_beam">
        <option value="mkat0"> MeerKAT I </option>
        <option value="mkat1"> MeerKAT II </option>
        <option value="mkat2"> MeerKAT III </option>
        <option value="kat7"> KAT-7 </option>
        <option value="wsrt"> WSRT </option>
        <option value="jvla"> JVLA </option>
      </td>
    </tr>
    <tr>
      <td>Feed Angle</td>
      <td><input type="text" name="ds_feed_angle"></td>
    </tr>
  </table>

  <h2 align="center">Corruptions</h2>
  <table style="width:700px" align="center" border=1 bgcolor="grey">
      <tr>
      <td>Amplitude Phase Gains</td>
      <td><input type="text" name="cr_amp_phase_gains"></td>
    </tr>
    <tr>
      <td>Pointing Errors</td>
      <td><input type="text" name="cr_pointing_error"></td>
    </tr>
    <tr>
      <td>RFI</td>
      <td><input type="text" name="cr_rfi"></td>
    </tr>
  </table>


  <h2 align="center">Imaging Settings</h2>

  <table style="width:700px" align="center" border=1 bgcolor="grey">
    <tr>
      <td>Number of Pixels</td>
      <td><input type="number" name="im_npix"></td>
    </tr>
    <tr>
      <td>Pixel Width</td>
      <td><input type="number" name="im_pixel">arcseconds</td>
    </tr>
    <tr>
      <td>UV-Weighing</td>
      <td>
        <select name="im_weight">
           <option value="natural">Natural </option>
           <option value="uniform">Uniform </option>
           <option value ="briggs">Briggs </option>
          </select>
      </td>
    </tr>
    <tr>
      <td>Weight FOV</td>
      <td><input type="number" name="im_weight_fov">arcminutes</td>
    </tr>
    <tr>
      <td>UV-Taper</td>
      <td><input type="text" name="im_taper"></td>
    </tr>
    <tr>
      <td>Number of W-Projection Planes to use</td>
      <td><input type="number" name="im_wprojplanes"></td>
    </tr>
    <tr>
      <td>Imaging Mode</td>
      <td>
        <select name="im_mode">
         <option value='channel'>Channel</option>
         <option value='mfs'>MFS</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Spectral Window</td>  <!-- Advanced Option--!>
      <td><input type="number" name="im_spwid"></td>
    </tr>
    <tr>
      <td>Number of Channels</td>  <!-- Advanced Option--!>
      <td>
        <input name="im_nchan" type="number">
        </input>
      </td>
    </tr>
    <tr>
      <td>Imager Channelise</td>  <!-- If option is custom, need to allow user to enter an integer--!>
      <td>
        <select name="channelise">
         <option value="NCHAN">Average all</option>
         <option value=1> 1 - Image every channel</option>
         <option value="custom">Custom</option>
        </select>
      </td>
    </tr>
    <tr>
<!--      <td>Start Channel</td>
      <td><input type="number" name="im_chanstart"></td>
    </tr>
    <tr>
      <td>Channel Step</td>
      <td><input type="number" name="im_chanstep"></td>
    </tr>
    <tr>
      <td>Image Number of Channels</td>
      <td><input type="number" name="im_img_nchan"></td>
    </tr>
    <tr>
      <td>Image Start Channel</td>
      <td><input type="number" name="im_img_chanstart"></td>
    </tr>
    <tr>
      <td>Image Channel Step</td>
      <td><input type="number" name="im_img_chanstep"></td>
    </tr> --!>
    <tr>  
      <td>Stokes</td>
      <td><input type="text" name="im_stokes"></td>
    </tr>
  </table>


  <h2 align="center">Deconvolution Settings</h2>

  <table style="width:700px" align="center" border=1 bgcolor="grey">
    <tr>
      <td>Clean</td>
      <td>
        <select name="clean">
          <option value="True">YES</option>
          <option value="False">NO</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Deconvolution Algorithm</td>
      <td>
        <select name="dc_operation">
          <option value="csclean">csclean</option>
          <option value="hogbom">hogbom</option>
          <option value="clark">clark</option>
          <option value="multiscale">multiscale</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Clean Scales</td>
      <td><input type="text" name="dc_usevector"></td>
    </tr>
    <tr>
      <td>Number of  Scales</td>
      <td><input type="number" name="dc_nscales"></td>
    </tr>

    <tr>
      <td>Number of Clean Iterations to use</td>
      <td><input type="number" name="dc_niter"></td>
    </tr>
    <tr>
      <td>Clean Threshold</td>
      <td><input type="text" name="dc_threshold"></td>
      <td>
        <select >
          <option value="mJy">mJy</option>
          <option value="Jy">Jy</option>
        </select>
      </td>
    </tr>

    </tr>
  </table>

  <table style="width:700px height:200px" align="center">
    <tr align="center"><td><input type="submit" name="submit"></td></tr>
  </table>

</form>
</font>

</body>
</html>
