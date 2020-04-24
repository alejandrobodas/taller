import netCDF4,argparse,sys
import numpy as np

def get_var_list(ncfile):
    dataset = netCDF4.Dataset(ncfile)
    var_list = dataset.variables.keys()
    dataset.close()
    return var_list
    

def read_var(fname, vname):
    f_id = netCDF4.Dataset(fname,'r')
    return f_id.variables[vname][:]

def calculate_stats(tst, kgo, atol=0.0, rtol=None):
    summary_stats = {'N':0, 'AvgDiff':0.0, 'MinDiff':0.0, 'MaxDiff':0.0, 'StDev':0.0}
    # All differences
    d = tst - kgo
    # Mask for differences larger than absolute tolerance
    maskAllDiff = (np.absolute(d) > atol)
    NallDiff = maskAllDiff.sum()
    # If there are differences larger than atol,
    # then calculate summary statsitics
    if (NallDiff > 0):
        diffs = d[maskAllDiff]
        # Are relative differences requested?
        if rtol is not None:
            # Calculate relative differences. When KGO=0,
            # use test as reference (i.e. relative diff will
            # be 1 or -1)
            maskedKgo = kgo[maskAllDiff]
            rdiffs = diffs / maskedKgo
            maks_zeroes = (maskedKgo == 0.0)
            rdiffs[mask_zeroes] = np.sign(diffs[mask_zeroes])
            # Keep only those diffs larger than relative tolerance
            diffs = diffs[np.absolute(rdiffs) > rtol]
            NallDiff = diffs.sum()
        # Calculate summary stats
        summary_stats['N'] = NallDiff
        summary_stats['AvgDiff'] = diffs.mean()
        summary_stats['MinDiff'] = diffs.min()
        summary_stats['MaxDiff'] = diffs.max()
        summary_stats['StDev'] = diffs.std()
        
    return summary_stats

def print_stats_table(summary_stats):
    for key, s in summary_stats.items():
        print(key,s)

#######################
# Main
#######################
if __name__ == '__main__':

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("kgo_file")
    parser.add_argument("tst_file")
    args = parser.parse_args()

    # Get list of variables
    kgo_vars = get_var_list(args.kgo_file)
    tst_vars = get_var_list(args.tst_file)
    nkgo = len(kgo_vars)
    ntst = len(tst_vars)

    # Dictionary for summary statistics
    summary_stats = {}

    # Iterate over shortest list and calculate stats
    errored = False
    if (nkgo <= ntst):
        vlst = kgo_vars
    else:
        vlst = tst_vars
    for vname in vlst:
        kgo = read_var(args.kgo_file, vname) # KGO
        tst = read_var(args.tst_file, vname) # test
        summary_stats[vname] = calculate_stats(tst, kgo)
        if summary_stats[vname]['N'] > 0: errored = True

    # Print summary stats
    print_stats_table(summary_stats)
    
    # Error if files have different number variables. If the number 
    # of variables is the same, but they have different names it will
    # fail summary_stats.
    if (nkgo != ntst):
        errored = True
        print("=== Variables in KGO ===")
        print(kgo_vars)
        print("=== Variables in Test ===")
        print(tst_vars)

    # Exit with correct error condition
    if errored:
        sys.exit(1)
    else:
        sys.exit()
