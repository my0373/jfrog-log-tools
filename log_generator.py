"""Artifactory Log Generator
    
This script exists to generate log files for testing purposes.

To show the available options, please run

log_generator.py -h

"""
import datetime
import os
from datetime import timedelta
import random
import argparse
from jfrog_utils.jfrog_logs import *
def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    
    # Add the -f option to specify the log file. If omitted, then stdout is used.
    parser.add_argument("-f", 
                        "--file",
                        help="specify the output file",
                        type=str,
                        required=True)
    
    # Add the -t option to optional pattern argument.
    parser.add_argument("-t", 
                        "--type", 
                        help="specify the log format to use. Example: 'v6', 'v7-in'",
                        default="v7-in",
                        type=str,
                        required=True)

    parser.add_argument("-p",
                        "--protocol",
                        help="specify the IP version to use 'ipv4', 'ipv6'",
                        default="ipv4",
                        type=str,
                        required=False)
    
    # Add the -d option to specify a date range
    parser.add_argument("-d", 
                        "--days", 
                        help="specify the number of days to spread the logs over",
                        default=10,
                        type=int,
                        required=False)
    
    parser.add_argument("-n", 
                        "--numlines", 
                        help="Number of lines to print",
                        default=10,
                        type=int,
                        required=True)
    
     
    return parser.parse_args()


def main():
    """
    Main function.
    """

    #TODO: change the ipv4 / v6 flags, and pass the function to call. This will avoid an if statement in the loop.

    # Delete any stale files and start writing.
    args = parse_arguments()


    try:
        os.remove(args.file)
    except FileNotFoundError:
        pass

    with open(args.file, "a") as logfile:

        if args.type == "v6":
            for lines in range(args.numlines):
                logfile.write(gen_v6_line(args.protocol) + '\n')
        elif args.type == "v7in":
            for lines in range(args.numlines):
                logfile.write(gen_v7in_line(args.protocol) + '\n')
        elif args.type == "v7out":
            for lines in range(args.numlines):
                logfile.write(gen_v7out_line(args.protocol) + '\n')
    
    
if __name__ == '__main__':
    main()