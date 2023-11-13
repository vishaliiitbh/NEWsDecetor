# this is also a part of software which automatically sends email to the provided reciever
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'your_email@gmail.com'
sender_password = 'your_password'
receiver_email = 'receiver_email@example.com'
subject = 'Automatic Email with Attachments'


attachment_dir = 'E:/New folder'# Directory containing files to attach
ministry=['Home','Income','Health','Education','None'] #list of ministry
mail_add={'Home':'joshi1012ivishal@gmail.com','Income':'shiwanst94@gmail.com','Health':'ivygag@niseko.ve','Education':'bhaunishank@gmail.com','None':'?'}

#check the files one by one
for m in ministry:
    # Substring to filter files
    substring_to_match = m  # Replace with your desired substring
    receiver_email=mail_add[m]
    # Create a list of attachment file paths that match the substring
    attachment_files = [os.path.join(attachment_dir, filename) for filename in os.listdir(attachment_dir) if
                        substring_to_match in filename]

    if not attachment_files:
        continue
    else:

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText('Please find the attached files.'))

        # Attach files
        for attachment_file in attachment_files:
            with open(attachment_file, 'rb') as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment_file))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_file)}"'
            message.attach(part)

        # Connect to the SMTP server
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email:", str(e))
