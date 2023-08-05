```
pip install microlog
```
# microlog
Simple and lightweight logging

## Getting started
```
from microlog import Logger
my_logs = Logger()
my_logs.log("Hello World!")
```
* Logs can be created with the following methods
  * `log()`
  * `debug()`
  * `info()`
  * `warning()`
  * `error()`
  * `critical()`
* Logs from a current session are saved in memory and can be viewed with the `logs()` method.

## Options
There are three options available when creating a new Logger instance.
### 1. File
By default a log file will not be created when creating a new Logger instance. Set the `file` parameter to `True` and a log file will be created in the current directory. You may provide a custom name for the log file by setting the `file` parameter to a string value.
```
Logger(file = "my_logs")
```
Logs are written using the append option so they can be added to existing log files.
### 2. Console
Log messages will be written to the console by default. Set the `console` parameter to `False` to stop seeing log messages in the console.
```
Logger(console = False)
```
You can change this status using the `console()` method.
```
my_logs.console(False)
```
### 3. Time format
All references to time will be local date-time by default. To use a UTC timestamp, set the `ts` parameter to `True`.  This will apply to default log file names and times in the log files.
```
Logger(ts = True)
```
