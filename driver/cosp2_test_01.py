import netCDF4,argparse,sys
import numpy as np

def read_var(fname, vname):
    f_id = netCDF4.Dataset(fname,'r')
    return f_id.variables[vname][:]

def calculate_stats(tst, kgo):
    # Compute relative difference.
    d = tst/kgo-1
    d[np.where(kgo == 0.0)] = 0.0
    # Relative difference = 1 if kgo = 0 and tst != kgo
    d[(kgo == 0.0) & (tst != kgo)] = 1.0    
    # Flag any point which exceeds error threshold. 
    error = np.argwhere(abs(d) >= 0.0)
    # Error fraction
    return float(len(error))/d.size

#######################
# Main
#######################
if __name__ == '__main__':

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("kgo_file")
    parser.add_argument("out_file")
    args = parser.parse_args()

    # Get list of variables
    dset = netCDF4.Dataset(args.kgo_file)
    vlst = dset.variables.keys()
    nvrs = len(vlst)
    dset.close()

    # Create variables for summary statistics
    fracError = np.zeros(nvrs) # Error fraction
    minError  = np.zeros(nvrs) # Minimum difference
    maxError  = np.zeros(nvrs) # Maximum difference

    # Loop over variables
    iv = 0
    for vname in vlst:
        print(vname)
        # Read variable
        kgo = read_var(args.kgo_file, vname) # KGO
        tst = read_var(args.out_file, vname) # test

        # Compare variable
        fracError[iv] = calculate_stats(tst, kgo)
        iv+=1
    
    s = fracError.sum()
