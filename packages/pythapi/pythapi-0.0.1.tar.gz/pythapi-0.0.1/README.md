# pythapi
pythapi is a micro framework written in Python to perform API calls. Currently it is a work in progress and all contributation are welcome.

# Contributing
Up to the challenge making this micro framework even better? Fork the repository and checkout the devel branch for local development.

Ready for a merge? Create a merge request from your devel branche to the original devel branche.

# Getting started example

```
import urllib3
import pythapi

# Disable certificate warnings and connect to destination API host
urllib3.disable_warnings()

# Specify the destination host and the base URL.
apiEndpoint = pyapi.Connect('localhost', '/base/api/url')

# Get all users
# This will perform a GET request using the URL https://localhost/base/api/url/users

apiEndpoint.get(/users)
```
