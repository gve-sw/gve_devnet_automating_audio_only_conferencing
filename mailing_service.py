# Copyright (c) 2023 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

class Mail():

    def __init__(self, sender_email, sender_password):
        
        self.sender_email = sender_email
        self.sender_password = sender_password


    def convert_template_file_to_custom_content(self, variables={}, base_file_path=""):

        file = open(base_file_path, "r")
        content = file.read()
        file.close()

        for variable in variables:
            content = content.replace("{"+str(variable)+"}", variables[variable])

        return content


    def create_email_content(self, receiver_email, host_access_code, attendee_access_code, host_pin_code, audio_pin_code, site_name):
        
        title = "Audioconferencing Information"

        variables = {
            "email": receiver_email,
            "host_access_code": host_access_code,
            "host_pin_code":host_pin_code,
            "attendee_access_code": attendee_access_code,
            "audio_pin_code": audio_pin_code,
            "site_url": f"https://{site_name}.webex.com/{site_name}/globalcallin.php"
        }

        htmlContent = self.convert_template_file_to_custom_content(variables=variables, base_file_path="templates/email_template.html")
        textContent = self.convert_template_file_to_custom_content(variables=variables, base_file_path="templates/text_template.txt")

        return title, htmlContent, textContent


    def send_mail(self, receiver_email, host_access_code, attendee_access_code, host_pin_code, audio_pin_code, site_name, attachment=False):

        print(f'--------------------Send email to participant: {receiver_email} -----------------------')

        title, html, text = self.create_email_content(receiver_email, host_access_code, attendee_access_code, host_pin_code, audio_pin_code, site_name)

        sender = self.sender_email

        # Create message container 
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = receiver_email

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Read image from current directory with name header.png
        fp = open('templates/header.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<header>')
        msg.attach(msgImage)
        
        #For sending additional pdf attachment:
        if attachment:
            with open(attachment, "rb") as fil:
                part3 = MIMEApplication(
                    fil.read(),
                    Name=basename(attachment)
                )
            part3['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
            msg.attach(part3)
        

        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login(sender, self.sender_password)
        mail.sendmail(sender, receiver_email, msg.as_string())
        mail.quit()