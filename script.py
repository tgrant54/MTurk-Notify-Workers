import hmac
import time
import argparse
import base64
import requests
from xml.etree import ElementTree as ET
from hashlib import sha1

access_key="" # Your AWSAccessKeyId
secret_access_key="" # Your AWSSecretKey

def makeRequest(worker, subject, message):
  url = "https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester"
  operation = "NotifyWorkers";
  timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime());
  hashed = hmac.new(secret_access_key, "AWSMechanicalTurkRequesterNotifyWorkers"+timestamp, sha1)
  signature = base64.encodestring(hashed.digest()).strip()
  
  # request body
  body = { "MessageText": message, "Subject": subject, "WorkerId.1": worker,
           "Operation": operation, "Version": "2014-08-15",
           "AWSAccessKeyId": access_key, "Signature": signature,
           "Timestamp": timestamp };
  
  response = requests.post(url, data=body)
  response.encoding = 'utf-8'
  
  if (response.status_code == 200):
    content = response.text.replace('urn:', '')
    root = ET.fromstring(content);
    for child in root:
      if (child.tag == 'Errors'):
        errorMsg = child[0][1]
        return [errorMsg.text]
      if (child.tag == 'NotifyWorkersResult'):
        for child2 in child:
          if (child2.tag == 'NotifyWorkersFailureStatus'):
            errorMsg = child2[1]
            return [errorMsg.text]
    return []
  else:
    return ['Failed Request']
    
def main(subject, message, workers):
  error_count = 0;
  success_count = 0;
  total = 0;
  
  # Read in workerIDs into worker_ids list
  workers_file = open(workers, 'r');
  worker_ids = workers_file.readlines();
  workers_file.close();
  
  for worker in worker_ids:
    total += 1;
    print 'Progress: ['+str(total)+'/'+str(len(worker_ids))+']'
    
    worker = worker.rstrip();
    res = makeRequest(worker, subject, message);
    #print res;
    if (len(res) > 0):
      # Error occured, log the workerID to error file
      error_count += 1;
      error_file = open("errors.txt", 'ab+');
      error_file.write(worker+': '+res[0]+'\n');
      error_file.close();
    else:
      # Success
      success_count += 1;
  
  print 'Finished: ['+str(success_count)+'/'+str(total)+'] successfull, '+str(error_count)+' errors';
  

parser = argparse.ArgumentParser(description='Send an email to a list of MTurk Workers');
parser.add_argument("workers_file", help="The file of MTurk worker ids.");
parser.add_argument("-s", "--subject", dest="subject", help="The subject for the email. If not specified, the program will prompt for this.");
parser.add_argument("-m", "--message", dest="message", help="The message for the email. If not specified, the program will prompt for this.");
args = parser.parse_args()

if (args.subject is None):
  args.subject = raw_input('Please enter the subject for the email: ');

if (args.message is None):
  args.message = raw_input('Please enter the message to be sent: ');
  
main(args.subject, args.message, args.workers_file);