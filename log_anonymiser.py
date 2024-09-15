"""Artifactory Log Anonymiser
    
This script exists to read a source log file and create anonymised output for support purposes.

To show the available options, please run

log_anonymiser.py -h

"""
from datetime import datetime
import os, sys
import argparse
from jfrog_utils.jfrog_logs import *


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    
    # Add the -f option to specify the log file. If omitted, then stdout is used.
    parser.add_argument("-o", 
                        "--outputfile",
                        help="specify the output file",
                        type=str,
                        required=True)
    
    # Add the -t option to optional pattern argument.
    parser.add_argument("-i", 
                        "--input", 
                        help="The source input file",
                        type=str,
                        required=True)
    
    parser.add_argument("-d",
                        "--debug",
                        help="Enable debug mode",
                        action="store_true",
                        required=False)

    return parser.parse_args()

def main():

    args = parse_arguments()

    logfile_version = get_logfile_version(args.input)

    if logfile_version == "v6":
        if args.debug:
            print("v6")
        anonymise_v6_logfile(args.input, args.outputfile)

    elif logfile_version == "v7in":
        if args.debug:
            print("v7in")
        anonymise_v7in_logfile(args.input, args.outputfile)
    
    # elif logfile_version == "v7out":
    #     if args.debug:
    #         print("v7out")
    #     anonymise_v7out_logfile(args.input, args.outputfile)

    else:
        if args.debug:
            print(f"Unknown log file version: {args.input}")
        sys.exit(1)
    
    
if __name__ == '__main__':
    main()