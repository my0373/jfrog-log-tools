from datetime import timedelta, datetime
from random import random, randint, choices

def anonymise_v6_logfile(input_logfile, output_logfile):
    """
    Anonymise a v6 log file.
    """
    try:
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
    except IndexError:
        return False


def anonymise_v7in_logfile(input_logfile, output_logfile):
    """
    Anonymise a v7in log file.
    """
    try:
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
    except IndexError:
        return False
        

def anonymise_v7out_logfile(input_logfile, output_logfile):
    """
    Anonymise a v7out log file.
    """
    #TODO: Implement this function
    return True

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
    #TODO: Update this function to look for more than just the first field. 
    # Both v7in and out share the same date so it can misidentify the version.

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
        

def get_random_dates(days=7) -> datetime:
    """
    Generate random dates.
    """
    start_date = datetime.now()
    end_date = start_date - timedelta(days=days)
# jfrog-ignore
    random_date = start_date + (end_date - start_date) * random()

    return random_date 

def get_fake_ipv4():
# jfrog-ignore
    return ".".join(map(str, (randint(0, 255) 
                        for _ in range(4))))

def get_fake_ipv6():
    M = 16**4
# jfrog-ignore
    return ":".join(("%x" % randint(0, M) for i in range(8)))

def get_random_user():
    userlist = ["admin",
                "anonymous",
                "crazydave",
                "upload_user",
                "jenkins",
                "non_authenticated_user"]
# jfrog-ignore    
    return userlist[randint(0,len(userlist) -1)]

def get_random_method():
    methods = ["DELETE","GET","HEAD","OPTIONS","PATCH","POST","PUT"]
# jfrog-ignore    
    return methods[randint(0,len(methods) -1)]

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
    return codes[randint(0,len(codes) -1)]

def get_random_content_length():
# jfrog-ignore
    return randint(0, 9999999999)
    
def gen_v6_line(protocol):
    timestamp = datetime.strftime(get_random_dates(days=7),
                  '%Y%m%d%H%M%S')
# jfrog-ignore
    request_duration = randint(1,1100)
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


def gen_v7in_line(protocol):
    """
    This is the definition of the request log format for v7 of the JFrog platform. The fields are as follow
    Timestamp | Trace ID | Remote Address | Username | Request method | Request URL | Return Status | Request Content Length | Response Content Length | Request Duration | Request User Agent
    
    The source for this information is https://jfrog.com/help/r/jfrog-platform-administration-documentation/request-log
    """
# jfrog-ignore
    timestamp = get_random_dates(days=7).isoformat()

# jfrog-ignore
    request_duration = randint(1,1100)
    request_traceid = ''.join(choices('0123456789abcdef', k=16))
    request_type = "REQUEST"
    # remote_address = get_fake_ipv4()
    remote_address = get_fake_ipv6() 
    username = get_random_user()
    request_method = get_random_method()
    request_url = "/home/" + get_random_user() + "/" + get_random_user() + ".zip"
    protocol_version = "HTTP/1.1"
    return_status = get_random_response_code()
    request_content_length = get_random_content_length()
    response_content_length = get_random_content_length()
    request_user_agent = "JFrog Access Java Client/4.1.12"

    
    line = f"{timestamp}|{request_traceid}|{remote_address}|{username}|{request_method}|{request_url}|{return_status}|{request_content_length}|{response_content_length}|{request_duration}|{request_user_agent}"
    return line 

def gen_v7out_line(protocol):
    """
    This is the definition of the request log format for v7 outbound request log of the JFrog platform. The fields are as follow
    Timestamp | Trace ID | Remote Repository Name | Username | Request method | Request URL | Return Status | Request Content Length | Response Content Length | Request Duration

    
    The source for this information is https://jfrog.com/help/r/jfrog-platform-administration-documentation/outbound-request-log
    """
# jfrog-ignore
    timestamp = get_random_dates(days=7).isoformat()

# jfrog-ignore
    request_duration = randint(1,1100)
    request_traceid = ''.join(choices('0123456789abcdef', k=16))
    request_repository_name = "generic-remote"
    request_type = "REQUEST"
    # remote_address = get_fake_ipv4()
    remote_address = get_fake_ipv6() 
    username = get_random_user()
    request_method = get_random_method()
    request_url = "/home/" + get_random_user() + "/" + get_random_user() + ".zip"
    protocol_version = "HTTP/1.1"
    response_code = get_random_response_code()
    request_content_length = get_random_content_length()
    response_content_length = get_random_content_length()

    
    line = f"{timestamp}|{request_traceid}|{request_repository_name}|{username}|{request_method}|{request_url}|{response_code}|{request_content_length}|{response_content_length}|{request_duration}"
    return line  