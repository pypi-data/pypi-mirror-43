::# do not print everything on screen ::
@each off  
::# project path ::
set dir=%~dp0
::# python script ::
set pyscpt=%dir%easycon
::#run script by python in env. Args are passed::  
python %pyscpt% %*
