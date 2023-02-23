import os

from model_translator.models import SwaksEmail, CrAssetEmulationAssetJoin, PalEmulationSoftwareModel


def swaks_executor(system_event):

    print("calling email executor-> " + system_event.__str__())
    # Fetch email event
    email_event = SwaksEmail.objects.filter(emaileventid=system_event.creventtypeid).first()

    # Fetch target emulation software
    emulation_software_ids = CrAssetEmulationAssetJoin.objects.values_list('emassetid').filter(
        crsystemeventid=system_event.crsystemeventid
    )
    # Fetch emulation software
    # TODO FOR NOW WE ASSUME 1 EMULATION SOFTWARE, THIS WILL BE EXTENDED TO SUPPORT MULTIPLE
    emulation_software = PalEmulationSoftwareModel.objects.filter(emulationsoftwaremodelid=emulation_software_ids[0][0])\
        .first()

    # From email event Fetch body, subject, emailserver, recipient, sender,malicious or not
    email_body = email_event.body
    email_subject = email_event.subject
    email_server = email_event.emailserver
    email_recipient = email_event.recipient
    email_sender = email_event.sender
    email_ismalicious = email_event.ismalicious
    email_recipient_final = email_recipient+"@"+email_server
    email_sender_final = email_sender+"@"+email_server

    # From emulation software Fetch target IP address
    target_ip = emulation_software.ipaddress

    if email_ismalicious:
        print("Preparing attack stage...")
        print("Sending malicious email... ")
        # command = 'swaks --from CEO@mail.server.org --body "Everybody login to the corporate google account and update
        # your security information, courtecy of the security team <a href="http:192.168.134.137:80">
        # https://secure.internal.google.server.org </a>" --h-Subject "Important Security Alert" --add-header
        # "MIME-Version: 1.0" --add-header "Content-Type: text/html" --to victim@mail.server.org'

        print("Sender: " + email_sender_final)
        print("Recipient: " + email_recipient_final)
        print("Subject: " + email_subject)
        print("Body: " + email_body)
        print("Malicious: " + email_ismalicious.__str__())
        command = 'swaks  --body "' + email_body + '" --h-Subject "' + email_subject \
                  + '" --add-header "MIME-Version: 1.0" --add-header "Content-Type: text/html" --to ' \
                  + email_recipient_final + ' --from ' \
                  + email_sender_final

        os.system(command)
    else:
        print("Sending benign email...")
        print("Sender: "+email_sender_final)
        print("Recipient: "+email_recipient_final)
        print("Subject: "+email_subject)
        print("Body: "+email_body)
        print("Malicious: "+email_ismalicious.__str__())
        command = 'swaks  --body "' + email_body + '" --h-Subject "' + email_subject\
                  + '" --add-header "MIME-Version: 1.0" --add-header "Content-Type: text/html" --to ' \
                  + email_recipient_final + ' --from ' \
                  + email_sender_final

        os.system(command)
