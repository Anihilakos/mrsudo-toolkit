#! /bin/python3

import argparse
import os
#import random
#from emulation_translator.models import *

parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("recipient")
parser.add_argument("sender")
parser.add_argument("email_server")
parser.add_argument("body")
parser.add_argument("subject")
parser.add_argument("ismalicious")

# parse the arguments
args = parser.parse_args()

email_recipient_final = args.recipient + "@" + args.email_server
email_sender_final = args.sender + "@" + args.email_server
if args.ismalicious == 'true':
    print("Preparing attack stage...")
    print("Sending malicious email... ")
    # command = 'swaks --from CEO@mail.server.org --body "Everybody login to the corporate google account and update
    # your security information, courtecy of the security team <a href="http:192.168.134.137:80">
    # https://secure.internal.google.server.org </a>" --h-Subject "Important Security Alert" --add-header
    # "MIME-Version: 1.0" --add-header "Content-Type: text/html" --to victim@mail.server.org'

    print("Sender: " + email_sender_final)
    print("Recipient: " + email_recipient_final)
    print("Subject: " + args.subject)
    print("Body: " + args.body)
    print("Malicious: " + args.ismalicious.__str__())
    command = 'swaks  --body "' + args.body + '" --h-Subject "' + args.subject \
                + '" --add-header "MIME-Version: 1.0" --add-header "Content-Type: text/html" --to ' \
                + email_recipient_final + ' --from ' \
                + email_sender_final
    os.system(command)

else:
    print("Sending benign email...")
    print("Sender: "+email_sender_final)
    print("Recipient: "+email_recipient_final)
    print("Subject: "+args.subject)
    print("Body: "+args.body )
    print("Malicious: "+args.ismalicious__str__())
    command = 'swaks  --body "' + args.body + '" --h-Subject "' + args.subject\
                + '" --add-header "MIME-Version: 1.0" --add-header "Content-Type: text/html" --to ' \
                + email_recipient_final + ' --from ' \
                 + email_sender_final

    os.system(command)

