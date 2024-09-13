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
  
def get_random_dates(days=7) -> datetime:
    """
    Generate random dates.
    """
    start_date = datetime.datetime.now()
    end_date = start_date - timedelta(days=days)
# jfrog-ignore
    random_date = start_date + (end_date - start_date) * random.random()

    return random_date 

def get_fake_ipv4():
# jfrog-ignore
    return ".".join(map(str, (random.randint(0, 255) 
                        for _ in range(4))))

def get_fake_ipv6():
    M = 16**4
# jfrog-ignore
    return ":".join(("%x" % random.randint(0, M) for i in range(8)))

def get_random_user():
    userlist = ["admin",
                "anonymous",
                "crazydave",
                "upload_user",
                "jenkins",
                "non_authenticated_user"]
# jfrog-ignore    
    return userlist[random.randint(0,len(userlist) -1)]
                    

def get_random_method():
    methods = ["DELETE","GET","HEAD","OPTIONS","PATCH","POST","PUT"]
# jfrog-ignore    
    return methods[random.randint(0,len(methods) -1)]
    
def get_random_response_code():
    codes = [200,
             201,
             202,
             204,
             302,
             400,
             401,
             403,
             404,
             405,
             500]
# jfrog-ignore
    return codes[random.randint(0,len(codes) -1)]

def get_random_content_length():
# jfrog-ignore
    return random.randint(0, 9999999999)
    
def gen_v6_line(protocol):
    timestamp = datetime.datetime.strftime(get_random_dates(days=7),
                  '%Y%m%d%H%M%S')
# jfrog-ignore
    request_duration = random.randint(1,1100)
    request_type = "REQUEST"
    # remote_address = get_fake_ipv4
    if protocol == "ipv4":
        remote_address = get_fake_ipv4()
    else:
        remote_address = get_fake_ipv6()

    username = get_random_user()
    request_method = get_random_method()
    request_url = "/home/" + get_random_user() + "/" + get_random_user() + ".zip"
    protocol_version = "HTTP/1.1"
    response_code = get_random_response_code()
    request_content_length = get_random_content_length()
    
    line = f"{timestamp}|{request_duration}|{request_type}|{remote_address}|{username}|{request_method}|{request_url}|{protocol_version}|{response_code}|{request_content_length}"
    return line

def gen_v7in_line():
# jfrog-ignore
    timestamp = get_random_dates(days=7).isoformat()
# jfrog-ignore
    request_duration = random.randint(1,1100)
    request_type = "REQUEST"
    # remote_address = get_fake_ipv4()
    remote_address = get_fake_ipv6() 
    username = get_random_user()
    request_method = get_random_method()
    request_url = "/home/" + get_random_user() + "/" + get_random_user() + ".zip"
    protocol_version = "HTTP/1.1"
    response_code = get_random_response_code()
    request_content_length = get_random_content_length()
    
    line = f"{timestamp}|{request_duration}|{request_type}|{remote_address}|{username}|{request_method}|{request_url}|{protocol_version}|{response_code}|{request_content_length}"
    return line  


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
                logfile.write(gen_v6_line() + '\n')
        elif args.type == "v7in":
            for lines in range(args.numlines):
                logfile.write(gen_v7in_line() + '\n')
    
    
if __name__ == '__main__':
    main()