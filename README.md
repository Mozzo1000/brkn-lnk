# brkn-lnk
brkn-lnk (broken link) is a link checker


# Usage
## Check single url

`brknlnk https://google.com`

## Check multiple urls
Multiple urls can be passed to the program, separated by spaces.

`brknlnk https://google.com https://bing.com`

## Check urls from CSV file
Passing a csv file will have the program read the file and check every link inside it.

`brknlnk urls.csv`

## Results
By default, a simple list with information on how many urls have passed, returned with warnings or failed to load
```
✅ Passed: 2
⚠️ Warning: 0
❌ Failed: 0
```
A more verbose output can be printed by using the flags `-o stdout-all,stdout-passed,stdout-warning,stdout-failed`.

## Explanation of results
|Status   |Explanation      | 
|----------|-------------|
|Passed |Any 2XX HTTP responsde code  |
|Warning |Other types of errors like bad ssl certificate or unability to connect to host for other reasons than HTTP response codes.  |
|Failed|Any HTTP response code between 3XX and 5XX  |

# Scope
- Provide url(s) and get back http status code.
- If multiple urls are provided they should be processed concurrently (default max 20 connections at a time).
- Configurable options.
- Clean printout to console when processing urls and when everything is finished.