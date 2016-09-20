import gdb

def get_text():
    """ Get start and end of main .text section 
        from info proc stat """
    info_proc_stat=gdb.execute('info proc stat', to_string=True)
    start_text=-1
    end_text=-1
    for line in info_proc_stat.split('\n'):
        line=line.split(":")
        if line[0]=='Start of text':
            start_text=int(line[1].strip(), 16)
        if line[0]=='End of text':
            end_text=int(line[1].strip(), 16)
    if start_text != -1 and end_text != -1:
        return start_text,end_text
    else:
        return -1,-1

class bor(gdb.Command):
    def __init__(self):
        self.status='off'
        self.action='break'
        super(bor, self).__init__('bor', gdb.COMMAND_SUPPORT)
    def state(self):
        return "Status of Break on Ret is "+self.status+"/"+self.action +\
                "\n   Change with bor on/off and bor break/print"
    def invoke(self, arg, from_tty):
        args=arg.split(" ")
        if arg=="":
            print self.state()
        if args[0]=='on':
            self.status='on'
        if args[0]=='off':
            self.status='off'
        if args[0]=='break':
            self.action='break'
        if args[0]=='print':
            self.action='print'

class boc(gdb.Command):
    def __init__(self):
        self.status='off'
        self.action='break'
        super(boc, self).__init__('boc', gdb.COMMAND_SUPPORT)
    def state(self):
        return "Status of Break on Call is "+self.status+"/"+self.action +\
                "\n   Change with boc on/off and boc break/print"
    def invoke(self, arg, from_tty):
        args=arg.split(" ")
        if arg=="":
            print self.state()
        if args[0]=='on':
            self.status='on'
        if args[0]=='off':
            self.status='off'
        if args[0]=='break':
            self.action='break'
        if args[0]=='print':
            self.action='print'

class go(gdb.Command):
    def __init__(self):
        self.BOR = bor()
        self.BOC = boc()
        #self.start_end='unset'
        super(go, self).__init__('go', gdb.COMMAND_SUPPORT)
    def invoke(self, arg, from_tty):
        def p_print(bocbor,disa):
            adr=disa['addr']
            asm=disa['asm']
            print "[+] BreakOn%s is ON: %s\t%s" % (bocbor,hex(adr).rstrip('L'),asm)
        #if self.start_end=='unset':
        start_text,end_text=get_text()
        #    self.start_end='set'
        if self.BOR.status=='off' and self.BOC.status=='off':
            print "BOR and BOC are off. Use Continue \'c\' instead"
        else:
            while True:
                trash_it=gdb.execute('stepi',to_string=True)
                frame = gdb.selected_frame()
                arch = frame.architecture()
                pc=gdb.selected_frame().pc()
                disa = arch.disassemble(pc)[0]
                #print disa
                if disa['asm'].startswith("call") and self.BOC.status=='on':
                    adr=disa['addr']
                    if adr > start_text and adr < end_text:
                        #I'm not in binary, I'm in libs
                        #Seems easier to debug with this
                        p_print("Call",disa)
                        if self.BOC.action=='break':
                            break
                if disa['asm'].startswith("ret") and self.BOR.status=='on':
                    adr=disa['addr']
                    if adr > start_text and adr < end_text:
                        p_print("Ret",disa)
                        if self.BOR.action=='break':
                            break
        
go()

