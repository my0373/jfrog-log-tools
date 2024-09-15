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

