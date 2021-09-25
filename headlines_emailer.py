#Import Libraries
import requests     #http requests
from bs4 import BeautifulSoup     #web-scraping
import smtplib    #send email
from email.mime.multipart import MIMEMultipart   #email body
from email.mime.text import MIMEText
import datetime   #datetime
import os

now = datetime.datetime.now()   
content = ""

#extracting hackernews stories
def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ''
    cnt += ('<b>Hacker News Top Stories:</b>\n'+'<br/>'+'-'*50+'<br/>')
    response = requests.get(url)
    content = response.content   
    soup = BeautifulSoup(content,"html.parser")
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + '\n' + '<br/>') if tag.text != 'More' else '')
        #print(tag.prettify) #find_all('span',attrs={'class':'sitestr'}))
    return cnt    

cnt = extract_news('https://news.ycombinator.com/news')
content += cnt
content += ('<br/>----------<br/>')
content += ('<br><br>End of Message')


# Send Email
print("Composing EMail...")

# update email details
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = os.environ.get('EMAIL_USER')
TO = os.environ.get('EMAIL_USER')
PASSWORD = os.environ.get('EMAIL_PASS')

#Create text/plain msg
msg = MIMEMultipart()
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

#Initiating Server
print("Initiating Server...")
server = smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(0)
server.ehlo()
server.starttls()  
server.login(FROM,PASSWORD)
server.sendmail(FROM,TO,msg.as_string())

print("Email Sent...")
server.quit()  