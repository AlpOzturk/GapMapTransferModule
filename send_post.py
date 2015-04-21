
import requests

from credentials import TRANSFER_URL

payload = {
  'name' : 'Tracy',
  'email' : 'tracy@email.com',
  'contactable' : 'true',
  'subscribable' : 'true',
  'date' : '2015-12-20',
  'birthday' : '1983-11-23',
  'gender' : 'male',
  'diagnosis' : 'ASD',
  'diagnosis_date' : '2001-12-20',
  'ados' : 'true',
  'adir' : 'true',
  'other_diagnosis_tool' : 'true',
  'city' : 'Palo Alto',
  'state' : 'California',
  'country' : 'United States',
  'zip_code' : '08544',
  'latitude' : '54.242345',
  'longitude' : '-23.42552',
  'resources' : '',
  'related_disorders' : '',
  'password' : 'abc123'
}

session = requests.session()
req = requests.post(URL, data=payload)
# Print response code.
print req