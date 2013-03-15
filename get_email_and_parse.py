# -*- coding:utf-8 -*-
import time
import StringIO
import imaplib
import email

from __init__ import my_import

class Imap4mail(object):

    def __init__(self,data,html=False):
        self.files = dict()
        msg = email.message_from_string(data)
        self.title = self.decode(msg.get("Subject"))
        self.sender = self.decode(msg.get("From"))
        self.date = self.get_format_date(msg.get("Date"))

        for part in msg.walk():
            if part.get_content_maintype() ==  'multipart':
                continue
            filename = part.get_filename()
            if not filename:
                if not html:
                    if part.get_content_subtype() != "plain":
                        continue
                self.body = self.decode_body(part)
            else:
                tmpfile = StringIO.StringIO()
                tmpfile.write(part.get_payload(decode=1))
                self.files[filename] = tmpfile

    def decode(self,text):
        decodefrag = email.Header.decode_header(text)
        title = ''
        for frag,enc in decodefrag:
            if enc:
                title += unicode(frag,enc)
            else:
                title += unicode(frag)
        return title

    def decode_body(self,text):
        charset = str(text.get_content_charset())
        body = ''
        if charset:
            body += unicode(text.get_payload(),charset)
        else:
            body = text.get_payload()
        return body

    def get_format_date(self,date_string):
        # format_pattern = '%a,%d%b%Y %H:%M:%S'
        # if date_string[0].isdigit():
        #     format_pattern = '%d%b%Y %H:%M:%S'
        # return time.strptime(date_string[0:-6],format_pattern)
        return date_string

def write_to_file(filename):
    def _write(text):
        with open(filename,'a+') as f:
            f.writelines(text)
    return _write

def parse(server,user,password,target,filename=None,check_all=False):
    server = "settings.{}".format(server)
    settings = my_import(server)
    mail = imaplib.IMAP4_SSL(settings.HOST,settings.PORT)
    print 'start parsing'
    print server,user,target
    try:
        mail.login(user,password)
    except imaplib.IMAP4.error,e:
        print e

    if check_all:
        mail.select()
    else:
        mail.select(settings.INBOX)

    status,data = mail.search(None,"({} {})".format(settings.FROM,target))

    email_list = []
    for num in data[0].split():
        num = int(num)

        try:
            status,doc = mail.fetch(num,"RFC822")
        except Exception,e:
            print e

        m = Imap4mail(doc[0][1])
        date = m.date
        from_name = m.sender
        title = m.title
        text = m.body
        email_list.append(['Date:{}\n'.format(date),'From:{}\n'.format(from_name.encode('utf8')),
                            'Title:{}\n'.format(title.encode('utf8')),'Content:{}\n'.format(text.encode('utf8')),'\n'])

    mail.close()
    mail.logout()

    filename= filename or '{}.txt'.format(target)
    sorted(email_list,key=lambda x:x[0])
    writer = write_to_file(filename)
    for obj in email_list:
        try:
            writer(obj)
        except Exception,e:
            print e

    return 'Done! written at {}'.format(filename)



