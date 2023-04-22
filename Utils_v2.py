import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from path import email_path

URL = "https://www.bestfightodds.com/"

sender_email = "combatnotifications@gmail.com"
paswrd = "vsfumwclhptvxbvz"
with open(email_path, "r") as f:
    receiver_email = f.read().strip()

message = MIMEMultipart("alternative")
message["Subject"] = "Line Move!"
message["From"] = sender_email
message["To"] = receiver_email

# def get_increase(orig, new):
#     p1 = 100/(orig+100)
#     p2 = 100/(new+100)
#     percentage = p1 - p2
#     return percentage
#
# def get_decrease(orig, new):
#     p1 = orig/(orig+100)
#     p2 = new/(new+100)
#     percentage = p1 - p2
#     return percentage



def get_increase(orig, new):
    total_change = new - orig
    percentage = (total_change / orig) * 100
    return percentage

def get_decrease(orig, new):
    total_change = orig - new
    percentage = (total_change / orig) * 100
    return percentage

def send_email(fnl: dict):
    name_1 = fnl.get("name_1")
    name_2 = fnl.get("name_2")
    ref_1 = fnl.get("ref_1")
    ref_2 = fnl.get("ref_2")
    refp_1 = fnl.get("refp_1")
    refp_2 = fnl.get("refp_2")
    html = """
    <!DOCTYPE html> 
        <html>
        <head>
        <style>
        #customers {
          font-family: Arial, Helvetica, sans-serif;
          border-collapse: collapse;
          width: 50%;
        }
        
        #customers td, #customers th {
          border: 1px solid #ddd;
          padding: 8px;
        }
        
        #customers tr:nth-child(even){background-color: #f2f2f2;}
        
        #customers tr:hover {background-color: #ddd;}
        
        #customers th {
          padding-top: 12px;
          padding-bottom: 12px;
          text-align: left;
          background-color: #04AA6D;
          color: white;
        }
        </style>
        </head>
        <body>
        
        <h1>Line Move</h1>
        
        <table id="customers">
          <tr>
            <th>Time</th>
            <th>"""+str(name_1)+"""</th>
            <th>"""+str(name_2)+"""</th>
          </tr>
          <tr>
            <td>Current</td>
            <td align="center">"""+str(ref_1)+"""</td>
            <td align="center">"""+str(ref_2)+"""</td>
          </tr>
          <tr>
            <td>Previous</td>
            <td align="center">"""+str(refp_1)+"""</td>
            <td align="center">"""+str(refp_2)+"""</td> 
          </tr>
        </table>

        https://www.bestfightodds.com/
        </body>
        </html>
    """

    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, paswrd)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
