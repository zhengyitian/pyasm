import os
f = open('tiao.pa')
l = f.readlines()
f2 = open('out.asm','w')

class glog():
    def __init__(self):
        self.tlog = ''
        self.dlog = ''
        self.blog = ''
        self.arrayList = []
        self.inteList = []
        self.strList = []
        
    def add(self,s):
        self.tlog += s+'\n'
    def dAdd(self,s):
        self.dlog += s+'\n'
    def bAdd(self,s):
        self.blog += s+'\n'
    def gen(self):
        ss = 'global  main\n'
        ss += 'extern printf\n'
        ss += ' section .text\n'
        ss += self.tlog
        ss += ' section .data\n'
        ss += self.dlog
        ss += ' section .bss\n'
        ss += self.blog
        return ss
    def getToken(self,s):
        if s in self.strList:
            return s
        if '[' not in s:
            return '[%s]'%s
        ol = s.split('[')
        inte = ol[1].replace(']','')
        self.add('mov r15,[%s]'%inte)
        return '[%s+8*r15]'%ol[0]
log = glog()

def dealArray(one): 
    one = one.replace(',',' ')
    one = one.replace('|',' ')
    ol = one.split()    
    if len(ol) == 3:
        log.bAdd(ol[1]+':')
        log.bAdd('resq '+ol[2])
        return
    ss = ''
    for one in ol[3:]:
        ss += one+','
    log.dAdd(ol[1]+':')
    log.dAdd('dq '+ss[:-1])
def   dealInte(one):
    one = one.replace(',',' ')
    one = one.replace('|',' ')
    ol = one.split()    
    if len(ol) == 2:
        log.bAdd(ol[1]+':')
        log.bAdd('resq 1')
        return

    log.dAdd(ol[1]+':')
    log.dAdd('dq '+ol[2])
def dealPrint(one):
    one = one.replace(',',' ')
    ol = one.split()    
    co = 0
    def temp(s):
        log.add('mov %s, '%s+log.getToken(ol[co]))
        if co+1>=len(ol):
            return False
        return True       
    l = ['rdi','rsi','rdx','rcx','r8','r9']
    for one in l:
        co += 1
        if not temp(one):
            break
    log.add('mov rax,0')
    log.add('call printf')
    
def dealString(one):
    ol = one.split()
    log.strList.append(ol[1])
    log.dAdd(ol[1]+':')
    log.dAdd('db '+ol[2])

def dealMov(one):
    ol = one.split()

log.add(' main:')
log.add('push r15')

for one in l:
    if one.startswith('#'):
        continue
    two = one.replace(' ','')
    two = two.replace('\n','')
    if not two:
        continue
    ol = one.split()
    if ol[0]=='array':
        dealArray(one)   
    if ol[0]=='inte':
        dealInte(one)
    if ol[0]=='string':
        dealString(one)
    if ol[0]=='printf':
        dealPrint(one)
    if ol[0]=='mov':
        dealMov(one)
        
            

log.add('pop r15')
log.add('ret')

ss = log.gen()
f2.write(ss)
f2.close()
os.system(' nasm -felf64 out.asm&&gcc out.o -no-pie -o a &&./a ')
