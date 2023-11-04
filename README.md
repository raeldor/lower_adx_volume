# lower_adx_volume
This is some rudimentary code to lower the volume on ADX files.  I wrote this to lower the volume on music in Persona 3 FES because I felt it was overpowering the voice sound level.  This code keeps the original file sizes, so there are no problems with LBAs when re-integrating into the ISO.

In order to extract and re-compile the ISO, CVM, etc. files I used the following tools...

  UltraISO
  
  cvm_tool
  
  CD/DVD-ROM Generator version 2.00

When re-assembling the ISO using CD/DVD-ROM Generator version 2.00, make sure the LBAs are the same as the original ISO.  To do this you will need to re-add the files again in the correct order, then export as IML.  After this, you can use UltraISO's 'Compile IML to ISO' feature.
