# MTurk Notify Workers
Easy to use script for sending the same email to a list of MTurk Workers.

### Requirements:
* Python >= 2.7
* [requests](https://github.com/kennethreitz/requests)

### Setup:
Before using this script there are **two** pre-requisites that must be met.

1. Your AWSAccessKeyId and AWSSecretKey must be set in script.py
2. A workers file that contains **one worker ID per line**
 
In order to set the AWSAccessKeyId and AWSSecretKey, open script.py and edit the associated variables to contain the values retrieved from your AWS console. Make sure these values are between the double quotes.

### Usage:
- To prompt the user for the subject and message of the email.

        python script.py workers_file.txt

- Specify the subject and message to avoid the prompt.

        python script.py workers_file.txt --subject "Subject" --message "Message goes here"