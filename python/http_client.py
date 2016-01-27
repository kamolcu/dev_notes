import json
import urllib2

# https://docs.python.org/2/howto/urllib2.html
# Call api and read response payload

req = urllib2.Request('http://alpha-apis-gateway.wemall-dev.com/pds/v2/merchants')
response = urllib2.urlopen(req)
print response.read()

