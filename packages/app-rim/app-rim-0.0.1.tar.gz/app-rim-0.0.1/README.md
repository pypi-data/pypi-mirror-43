# app-rim
Application Runtime Image Managerc - python module enabling to manage
( backup , restore, organize ) files that get created durring usage 
of applications in users profile dir. This module primarly targets 
linux environments, it may work in other setups. Support for thoose 
might be added in future

## Background

In linux each system user is associated with user profile dir. Next
when a user uses an application like dropbox ( or others ) a subdir
in profile is created named ".dropbox" and it stores the user 
configuration of application as well as logs or other stuff app
needs to work properly. 

## Goal

This project aims to build a python module that will allow the 
following:

1) Create a tar archive of application configuration ( accounting for 
diffrent location of this files ie. ".config", ".local/share" ). 
2) allow restoration from backup stored in a globally defined backup 
dir
3) Provide the means to reconfigure existing application files into 
  directory hierarchy that is more compatible with xdg definition
  ( configuration files go into .config temporary, files go into  
    .cache, logs go into var/log, others go into .local/share )

4) Provied means to detec what applications have been used by user
   based on what configuration files have been created ( carefully 
   crafting a list of known non aplication dirs ie. 
   .loca/share/application )
