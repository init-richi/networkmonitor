########################################################################
#
# written by Richard Mietz in year 2016
# Networkmonitor 0.1
# Program for pinging Servers/Accesspoints and sending Statusmails
# written in Python 3.5
#
########################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

import time, os, smtplib
from email.mime.text import MIMEText

t = time.localtime()
date = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2])
logdata_time = "["+date+"] ["+str(t[3])+":"+str(t[4])+":"+str(t[5])+"]"

with open('config.txt', 'r') as config:
    config = config.readlines()
    for line in config:
        if 'FromMail:' in line:
            global fromMail
            fromMail = line.split()[1]
        if 'FromServer:' in line:
            global fromServer
            fromServer = line.split()[1]
        if 'FromPort:' in line:
            global fromPort
            fromPort = int(line.split()[1])
        if 'FromUser:' in line:
            global fromUser
            fromUser = line.split()[1]
        if 'FromPasswd:' in line:
            global fromPasswd
            fromPasswd = line.split()[1]
        if 'ToMail:' in line:
            global toMail
            toMail = line.split()[1]
        if 'SSL:' in line:
            global ssl
            if '1' in line.split()[1]:
                ssl = True
            else:
                ssl = False
        if 'TLS:' in line:
            global tls
            if '1' in line.split()[1]:
                tls = True
            else:
                tls = False
        if 'Location' in line:
            global location
            location = line.split()[1]

def main():
    ### read out ips.txt and ping/port test
    with open("ips.txt", "r") as ip_file:
        ips = ip_file.readlines()
    for item in ips:
        ip = item
        if '\n' in ip:
            ip = ip[0:-1]
        ip_upstatus = os.system("ping -c 1 " + ip)
        if ip_upstatus == 0:
            with open("mail.tmp", "a") as mail_tmp:
                mail_tmp.write(logdata_time + "[log_monitor_ping_success] - "+ip+ " reachable: True\r\n")
        elif ip_upstatus == 1:
            with open("mail.tmp", "a") as mail_tmp:
                mail_tmp.write(logdata_time + "[log_monitor_ping_success] - "+ip+ " reachable: No Response\r\n")
        else:
            with open("mail.tmp", "a") as mail_tmp:
                mail_tmp.write(logdata_time + "[log_monitor_ping_error] - "+ip+ " reachable: False\r\n")


def sendMail(user, pwd, to, subject, text):
    msg = MIMEText(text.encode('utf-8'),'plain','utf-8')
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject

    try:
        global smtpServer
        if ssl == True:
            smtpServer = smtplib.SMTP_SSL(fromServer, fromPort)

        else:

            smtpServer = smtplib.SMTP(fromServer, PORTNUMBER_AS_INT)

        if tls == True:
            smtpServer.ehlo()
            smtpServer.starttls()
        smtpServer.ehlo()
        smtpServer.login(fromUser, pwd)
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print("[+] Mail Sent Successfully.")

    except:
        print("[-] Sending Mail Failed.")

########################################################################################################################

main()
with open("mail.tmp", "r") as mail_tmp:
    sendMail(fromMail, fromPasswd, toMail, 'Statusmail Location: "' + location + '" ' + logdata_time, mail_tmp.read())
os.remove('mail.tmp')

