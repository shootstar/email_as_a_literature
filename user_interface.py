import re
import Tkinter
from get_email_and_parse import parse

FIELDS = 'user','password','target','save at'
NOT_SHOWING = ['password']

class BadValueError(Exception):
    pass

def onClick(entries):
    user,password,target,directory = [e[1].get() for e in entries]

    try:
        host,user,password,target,directory = check_value(user,password,target,directory)
    except BadValueError:
        print 'error'
        return False

    result = parse(host,user,password,target,directory)
    print result
    return True

def check_value(user,password,target,directory):
    if not re.search('@',user):
        raise BadValueError
    # if not re.search('@',target):
    #     raise BadValueError
    host = user.split('@')[1].split('.')[0]

    return host,user,password,target,directory

def makeform(root,fields):
    entries = list()
    for field in fields:
        row = Tkinter.Frame(root)
        lab = Tkinter.Label(row,width=15,text=field,anchor='w')
        if field in NOT_SHOWING:
            ent = Tkinter.Entry(row,show="*")
        else:
            ent = Tkinter.Entry(row)
        row.pack(side=Tkinter.TOP,fill=Tkinter.X,padx=5,pady=5)
        lab.pack(side=Tkinter.LEFT)
        ent.pack(side=Tkinter.RIGHT,expand=Tkinter.YES,fill=Tkinter.X)
        entries.append((field,ent))
    return entries

if __name__ == "__main__":
    root = Tkinter.Tk()
    ents = makeform(root,FIELDS)
    b1 = Tkinter.Button(root,text='submit',command=(lambda e=ents:onClick(e)))
    b1.pack(side=Tkinter.LEFT,padx=5,pady=5)
    b2 = Tkinter.Button(root,text='Quit',command=root.quit)
    b2.pack(side=Tkinter.LEFT,padx=5,pady=5)
    root.mainloop()

