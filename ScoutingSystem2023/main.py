# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import atexit
import os

from Calculator import Calculetor
from Initializer import Initializer
from Ranker import Ranker
from Repository import Repository
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def reversString(s):
    return s[::-1]


def convertComment(s):
    if s == 'intake':
        return reversString("הערות איסוף:")
    if s == 'field':
        return reversString("הערות מגרש:")
    if s == 'climb':
        return reversString("הערות טיפוס")
    if s == 'defence':
        return reversString("הערות הגנה:")
    if s == 'other':
        return reversString("הערות נוספות:")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


repo = Repository()
initializer = Initializer(repo)
calculetor = Calculetor(repo)
ranker = Ranker(repo)
atexit.register(repo.close)


def page1(matchNumber, my_pdf):
    my_pdf.add_page()
    my_pdf.set_font("Courier", size=16)
    text = "DATA PAGE ON GAME NUMBER " + str(matchNumber)
    my_pdf.cell(200, 10, txt=text, ln=1, align="L")
    my_pdf.image('logo.png', x=160, y=5, w=40, h=40)
    my_pdf.set_font("Courier", size=9)
    p1 = ranker.prepareMatch(matchNumber, False)
    my_pdf.multi_cell(200, 10, txt="\n\n", border=0, align="L")
    my_pdf.multi_cell(200, 6, txt=p1[0], border=0, align="L")
    if p1[1] == "EXPECTED RED ALLIANCE WIN!\n":
        my_pdf.set_text_color(255, 0, 0)
    else:
        my_pdf.set_text_color(0, 0, 255)
    my_pdf.multi_cell(200, 6, txt=p1[1], border=0, align="L")
    my_pdf.set_text_color(0, 0, 0)


def page2(teamNumber, my_pdf,color):
    my_pdf.add_page()
    my_pdf.set_font("Courier", size=16)
    if color == "r":
        my_pdf.set_text_color(255, 0, 0)
    if color == "b":
        my_pdf.set_text_color(0, 0, 255)
    text = "FULL INFO ON TEAM " + str(teamNumber)
    my_pdf.cell(200, 10, txt=text, ln=1, align="L")
    my_pdf.set_text_color(0, 0, 0)
    my_pdf.image('logo.png', x=160, y=5, w=40, h=40)
    my_pdf.set_font("Courier", size=8)
    my_pdf.multi_cell(200, 7, txt="\n\n", border=0, align="L")
    p2 = calculetor.printTeamFullInfo(teamNumber, False)
    j = 0
    y = 0
    finalY = 0
    for i in p2:
        j += 1
        if j % 2 == 0:
            my_pdf.set_xy(110, y)
        else:
            y = my_pdf.get_y()
        if j % 5 == 0:
            my_pdf.add_page()
            my_pdf.image('logo.png', x=160, y=5, w=40, h=40)
            my_pdf.multi_cell(200, 10, txt="\n\n\n", border=0, align="L")
            y = my_pdf.get_y()
            finalY = y

        my_pdf.multi_cell(100, 5, txt=i, border=0, align="L")
        finalY = max(finalY, my_pdf.get_y())
        if j % 2 == 0:
            my_pdf.set_y(finalY)
            my_pdf.multi_cell(200, 10, txt="\n", border=0, align="L")


def page3(teamNumber, my_pdf):
    w = 210
    calculetor.showGraph(teamNumber, False)
    my_pdf.add_page()
    my_pdf.image('logo.png', x=160, y=5, w=40, h=40)
    my_pdf.multi_cell(200, 10, txt="\n\n", border=0, align="L")
    my_pdf.set_font("Courier", size=16)
    t = "Graph Data " + str(teamNumber)
    my_pdf.multi_cell(200, 10, txt=t, border=0, align="C")
    t = str(teamNumber)+"1.png"
    my_pdf.image(t, x=10, y=45, w=100, h=70)
    os.remove(t)
    t = str(teamNumber) + "2.png"
    my_pdf.image(t, x=110, y=45, w=100, h=70)
    os.remove(t)
    t = str(teamNumber) + "3.png"
    my_pdf.image(t, x=70, y=116, w=100, h=70)
    os.remove(t)
    my_pdf.line(x1=0, y1=185, x2=w, y2=185)
    my_pdf.set_xy(10, 186)
    my_pdf.set_font('DejaVu', size=10)
    txt = "הערות:"
    my_pdf.multi_cell(200, 7, txt=reversString(txt), border=0, align="R")
    my_pdf.set_font('DejaVu', size=8)
    comments = calculetor.getComments(teamNumber)
    j = 0
    y = 0
    finalY = 0
    my_pdf.set_x(w-20)
    for i in comments.keys():
        j += 1
        if j % 2 == 0:
            my_pdf.set_xy(0, y)
        else:
            y = my_pdf.get_y()
            my_pdf.set_x(105)
        txt = convertComment(i)
        x = my_pdf.get_x()
        my_pdf.multi_cell(105, 5, txt=txt, border=0, align="R")
        for p in comments[i]:
            my_pdf.set_x(x)
            t = reversString(p)
            my_pdf.multi_cell(105, 5, txt=t, border=0, align="R")
        finalY = max(finalY, my_pdf.get_y())
        if j % 2 == 0:
            my_pdf.set_y(finalY)
            my_pdf.multi_cell(200, 3, txt="\n", border=0, align="R")


def pdfDataCreator(matchNumber):
    my_pdf = FPDF()
    my_pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    red = repo.alliances.findRed(matchNumber)
    page1(matchNumber, my_pdf)
    for i in red:
        page2(i[0], my_pdf,"r")
        page3(i[0], my_pdf)
    blue = repo.alliances.findBlue(matchNumber)
    for i in blue:
        page2(i[0], my_pdf,"b")
        page3(i[0], my_pdf)
    name = "Prepare Match " + str(matchNumber) + ".pdf"
    my_pdf.output(name)
    return name


def sendMail(filename):
    smtp_port = 587  # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    # Set up the email lists
    email_from = "eldadvask@gmail.com"
    email_list = "roboactive2096@gmail.com"

    # Define the password (better to reference externally)
    pswd = "luhnhevclkgosicb"  # As shown in the video this password is now dead, left in as example only

    # name the email subject
    subject = "system automat mail"
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_list
    msg['Subject'] = subject
    attachment = open(filename, 'rb')
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload(attachment.read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)
    text = msg.as_string()
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    TIE_server.sendmail(email_from, email_list, text)
    TIE_server.quit()


def nameOfFile(num):
    return "Prepare Match " + str(num) + ".pdf"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #לפני שרוצים להפעיל משהו אז להוריד אותו מהערה שזה אומר להוריד את ה# לפני השורה ולשים בסוגריים מה שצריך אם צריך.
    #calculetor.printTeamFullInfo(2096)
    #להכניס בסוגריים את המספר משחק מדפיס נתונים מלאים על קבוצה מסויימת
    ranker.rank()
    #ידפיס את הדירוגים
    #ranker.prepareMatch(11)
    #להכניס את המספר משחק בסוגריים מדפיס את הנתונים על המשחק
    #initializer.insertInfo()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
