from datetime import datetime
import os
import argparse
import sys

def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()

    # Add the -o option to specify the output directory.
    parser.add_argument("-o",
                        "--outputdir",
                        help="Specify the output directory",
                        type=str,
                        required=True)

    # Add the -i option to specify the input file or directory.
    parser.add_argument("-i",
                        "--input",
                        help="The source input file or directory",
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
    try:
        with open(logfile, "r") as log:
            first_line = log.readline()
            if validate_v6_line(first_line):
                return "v6"
            elif validate_v7in_line(first_line):
                return "v7in"
            else:
                return "unknown"
    except Exception as e:
        print(f"Error reading {logfile}: {e}")
        return "error"

def validate_v6_line(first_line):
    """
    Validate the first line of a log file to check the version.
    """
    date_str = first_line.split("|")[0]

    try:
        # Set the expected string format
        date_format = '%Y%m%d%H%M%S'
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def validate_v7in_line(first_line):
    """
    Validate the first line of a v7in log file.
    """
    timefield = first_line.split("|")[0]

    try:
        # Standard ISO datetime format
        datetime.fromisoformat(timefield)
        return True
    except ValueError:
        return False

def anonymise_v6_logfile(input_logfile, output_logfile, debug=False):
    """
    Anonymize v6 log files.
    """
    with open(input_logfile, "r") as infile, open(output_logfile, "w") as outfile:
        for line in infile:
            tmpline = line.split("|")

            # Check if the line has enough fields
            if len(tmpline) < 10:
                if debug:
                    print(f"Skipping malformed line (v6): {line.strip()}")
                continue

            anonymised_line = f"{tmpline[0]}|{tmpline[1]}|{tmpline[2]}|ADDRESS_REDACTED|USER_REDACTED|{tmpline[5]}|URL_REDACTED|{tmpline[7]}|{tmpline[8]}|{tmpline[9]}\n"
            outfile.write(anonymised_line)

            if debug:
                print(f"Anonymised v6 log line: {anonymised_line.strip()}")

def anonymise_v7in_logfile(input_logfile, output_logfile, debug=False):
    """
    Anonymize v7in log files.
    """
    with open(input_logfile, "r") as infile, open(output_logfile, "w") as outfile:
        for line in infile:
            tmpline = line.split("|")

            # Check if the line has enough fields
            if len(tmpline) < 11:
                if debug:
                    print(f"Skipping malformed line (v7in): {line.strip()}")
                continue

            anonymised_line = f"{tmpline[0]}|{tmpline[1]}|ADDRESS_REDACTED|USER_REDACTED|{tmpline[4]}|URL_REDACTED|{tmpline[6]}|{tmpline[7]}|{tmpline[8]}|{tmpline[9]}|{tmpline[10]}\n"
            outfile.write(anonymised_line)

            if debug:
                print(f"Anonymised v7in log line: {anonymised_line.strip()}")

def anonymise_v7out_logfile(input_logfile, output_logfile, debug=False):
    """
    Placeholder function for v7out log anonymization.
    """
    pass

def process_log_file(input_file, output_dir, unprocessed_files, debug=False):
    """
    Process and anonymize a single log file.
    """
    logfile_version = get_logfile_version(input_file)

    # Generate the output file path based on the input file name.
    output_file = os.path.join(output_dir, os.path.basename(input_file))

    if logfile_version == "v6":
        print(f"Processing v6 log file: {input_file}")
        anonymise_v6_logfile(input_file, output_file, debug)
    elif logfile_version == "v7in":
        print(f"Processing v7in log file: {input_file}")
        anonymise_v7in_logfile(input_file, output_file, debug)
    elif logfile_version == "v7out":
        print(f"Processing v7out log file: {input_file}")
        anonymise_v7out_logfile(input_file, output_file, debug)
    elif logfile_version == "unknown" or logfile_version == "error":
        print(f"Unknown or error in log file version: {input_file}")
        unprocessed_files.append(input_file)

def main():
    args = parse_arguments()

    # List to keep track of files with unknown or unprocessable versions.
    unprocessed_files = []

    # Check if input is a directory or a single file.
    if os.path.isdir(args.input):
        input_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input, f))]
    else:
        input_files = [args.input]

    # Ensure output directory exists.
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    # Process each input file.
    for input_file in input_files:
        process_log_file(input_file, args.outputdir, unprocessed_files, args.debug)

    # Output list of files that couldn't be processed.
    if unprocessed_files:
        print("\nThe following log files could not be processed due to unknown version or errors:")
        for file in unprocessed_files:
            print(f"  - {file}")

if __name__ == '__main__':
    main()