"""Artifactory Log Anonymiser
    
This script exists to read a source log file and create anonymised output for support purposes.

To show the available options, please run

log_anonymiser.py -h

"""
from datetime import datetime
import os
import argparse

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
  
def get_logfile_version(logfile):
    """
    Get the version of the log file.
    """
    with open(logfile, "r") as log:

        first_line = log.readline()
        if validate_v6_line(first_line):
            return "v6"
        elif validate_v7in_line(first_line):
            return "v7in"
        else:
            return "unknown"
        
        

def validate_v6_line(first_line):
    """
    Validate the first line of a log file to check the version
    """
    # Get the date string from the first line
    date_str =  first_line.split("|")[0]

    # test if the date string is in the correct format for a v6 file.
    try:
        # Set the expected string format
        date_format = '%Y%m%d%H%M%S'

        date_obj = datetime.strptime(date_str, date_format)
    except ValueError:
        return False
    
    return True 

def validate_v7in_line(first_line):
    timefield =  first_line.split("|")[0]

    try:

        # Example with the standard date and time format
        date_format = '%Y-%m-%d %H:%M:%S'

        date_obj = datetime.fromisoformat(timefield)
        print(date_obj)

        # Example with a different format

        date_str = '02/28/2023 02:30 PM'
        date_format = '%m/%d/%Y %I:%M %p'

        date_obj = datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def anonymise_v6_logfile(input_logfile, output_logfile):
    with open(input_logfile, "r") as infile, open(output_logfile, "w") as outfile:
        for line in infile:
            tmpline = line.split("|")
            timestamp = tmpline[0]
            request_duration = tmpline[1]
            request_type = tmpline[2]
            remote_address = "ADDRESS_REDACTED"
            username = "USER_REDACTED"
            request_method = tmpline[5]
            request_url = "URL_REDACTED"
            protocol_version = tmpline[7]
            response_code = tmpline[8]
            request_content_length = tmpline[9]
            
            anonymised_line = f"{timestamp}|{request_duration}|{request_type}|{remote_address}|{username}|{request_method}|{request_url}|{protocol_version}|{response_code}|{request_content_length}\n".strip()
            outfile.write(anonymised_line + '\n')
        


def anonymise_v7in_logfile(input_logfile, output_logfile):
    with open(input_logfile, "r") as infile, open(output_logfile, "w") as outfile:
        for line in infile:
            tmpline = line.split("|")
            timestamp = tmpline[0]
            request_traceid = tmpline[1]
            remote_address = "ADDRESS_REDACTED"
            username = "USER_REDACTED"
            request_method = tmpline[4]
            request_url = "URL_REDACTED"
            return_status = tmpline[6]
            request_content_length = tmpline[7]
            response_content_length = tmpline[8]
            request_duration = tmpline[9]
            request_user_agent = tmpline[10]
            
            anonymised_line = f"{timestamp}|{request_traceid}|{remote_address}|{username}|{request_method}|{request_url}|{return_status}|{request_content_length}|{response_content_length}|{request_duration}|{request_user_agent}"
    
            outfile.write(anonymised_line.strip() + '\n')
        

def anonymise_v7out_logfile(input_logfile, output_logfile):
    #TODO: Implement this function
    pass

def main():

    args = parse_arguments()

    logfile_version = get_logfile_version(args.input)

    if logfile_version == "v6":
        print("v6")
        anonymise_v6_logfile(args.input, args.outputfile)

    if logfile_version == "v7in":
        print("v7in")
        anonymise_v7in_logfile(args.input, args.outputfile)
    
    if logfile_version == "v7out":
        print("v7out")
        anonymise_v7out_logfile(args.input, args.outputfile)

    else:
        print(f"Unknown log file version: {args.input}")
        sys.exit(1)
    
    
if __name__ == '__main__':
    main()