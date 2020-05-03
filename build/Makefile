# Paths to source codes in COSP library
SRC_PATH     = ../src

# Standalone driver
DRIVER = ../driver/src
VPATH += $(DRIVER)

# Makefile.conf needs to define $(F90), $(F90FLAGS), $(NC_LIB), $(NC_INC)
include Makefile.conf
F90FLAGS += $(NC_INC)
LDFLAGS  += $(NC_LIB) -lnetcdff

# Rules
%.o: %.F90
	$(F90) $(F90FLAGS) -c $<

%.o: %.f90
	$(F90) $(F90FLAGS) -c $<

%: %.o
	$(F90) $(F90FLAGS) -o $@ $^ $(LDFLAGS) $(LIBS)

clean:
	rm -f *.mod *.o taller

driver:
	make taller
	mv taller ../driver/run
