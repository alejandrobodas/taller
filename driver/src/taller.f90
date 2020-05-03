PROGRAM TALLER
   use netcdf
   implicit none
   
   integer :: ierr,ncid,dimid,idx,idy
   real :: x(7), y(7)
   character(len = 80)  :: strerror
   x = 1.0
   y = 2.0
   
   ierr = nf90_create(path="../data/outputs/taller_out.nc", cmode=NF90_WRITE, &
            ncid=ncid)

   IF (ierr /= NF90_NOERR) THEN
      PRINT*, '   Problem opening netCDF file: '
      PRINT*, 'ierr:  ', ierr
      PRINT*, 'NF90_WRITE:  ', NF90_WRITE
      PRINT*, 'NF90_CLOBBER:  ', NF90_CLOBBER
      PRINT*, 'NF90_NOCLOBBER:  ', NF90_NOCLOBBER
      PRINT*, 'NF90_NOERR:  ', NF90_NOERR
      strerror =  nf90_strerror(ierr)
      print*, 'ERROR:  ', strerror
      STOP
   END IF

   ierr = nf90_def_dim(ncid, 'dx', 7, dimid)
   ierr = nf90_def_var(ncid, 'x', nf90_float, (/dimid/), idx)
   ierr = nf90_def_var(ncid, 'y', nf90_float, (/dimid/), idy)
   ierr = nf90_enddef(ncid)
   ierr = nf90_put_var(ncid, idx, x,count=(/7/))
   ierr = nf90_put_var(ncid, idy, y,count=(/7/))
   ierr = nf90_close(ncid) 
END PROGRAM TALLER

