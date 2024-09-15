# jfrog-log-tools
Some tools for working with logs.

## Disclaimer
This project is not supported, or endorsed by JFrog in any way. All scripts are for use at your own risk.

## Request log tools

### Logfile generation for testing
Often for testing we need to create some sample logfiles. The script ```log_generator.py``` allows us to create a specific logfile format.

* ```-f``` the filename to create
* ```-t``` the file format to create (currently ```v6```,```v7in```,```v7out``` options are supported)
* ```-n``` the number of lines to generate
* ```-p``` the version if IP to use. Currently ```ipv4``` and ```ipv6``` are supported.
* ```-d``` the duration in days to generate the requests from.

In this example we generate a log called matt.log with the a v7in log type, 10 million rows using IPv4 over a time period of 14 days.

```shell
python log_generator.py -f matt.log -t v7in -n 10000000 -p ipv4 -d 14
```

### Logfile anonymisation

The anonymisation script takes a single input request file (yes, I need to implement globbing and path walking.), detects the version (v6/v7) and writes it out to a target file with sensitive fields redacted.

The redacted fields are...

* remote_address
* username 
* urls

```shell 
python log_anonymiser.py -i inputlog.log -f output.log
```

## Build a docker container

```
podman build -t jfrog-log-tools .
```

### Run the image interactively
In this example, we'll run the container interactively with two volumes.

1. ```${HOME}/Downloads/logs``` will be mounted in the container, read only as ```/sourcelogs``` respecting SELinux contexts.
2. ```/tmp/destlogs/``` will be mounted in the container, read write as ```/destlogs``` respecting SELinux contexts.

We'll run bash as the entrypoint so we can "login" to the container.

```shell
$ docker run -it  \
--rm \
-v ${HOME}/Downloads/logs/:/sourcelogs:ro,Z  \
-v /tmp/destlogs/:/destlogs:Z  \
--entrypoint=/bin/bash  \
localhost/jfrog-log-tools \
-i
```

### Run one of the scripts
After logging in, we can run the scripts manually without any risk of overwriting the original logs.
```shell
root@0b8bd99aa74c:/code# python ./log_anonymiser.py -i /sourcelogs/v7-ipv4.log -o /destlogs/requestprocessed.log 
2024-09-11 19:23:20.782144
root@0b8bd99aa74c:/code# 
```

### Test the output and exit the container
We can test the output here 
```shell
root@0b8bd99aa74c:/code# head -1 /destlogs/requestprocessed.log

2024-09-11T19:23:20.782144|ab7acd630aa9a21d|ADDRESS_REDACTED|USER_REDACTED|GET|URL_REDACTED|201|3805396537|7827564335|385|JFrog Access Java Client/4.1.12
```

We can then exit the container with the command
```shell
root@0b8bd99aa74c:/code# exit
exit
```

We can also test the file exists after we exit the container.
```shell
$ head -1 /tmp/destlogs/requestprocessed.log
2024-09-11T19:23:20.782144|ab7acd630aa9a21d|ADDRESS_REDACTED|USER_REDACTED|GET|URL_REDACTED|201|3805396537|7827564335|385|JFrog Access Java Client/4.1.12
```