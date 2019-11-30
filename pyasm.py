import os
from collections import deque
f = open('tiao.pa')
l = f.readlines()
f.close()

class glog():
    def __init__(self):
        self.tlog = ''
        self.dlog = ''
        self.blog = ''
        self.arrayList = []
        self.inteList = []
        self.strList = []
        self.labelCo = 0
        self.ifcache = deque()
        self.elsecache = deque()
        self.whilecache = deque()
    def getLabel(self):
        self.labelCo += 1
        return 'label'+str(self.labelCo)
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
            if s not in self.inteList:
                return s
            return '[%s]'%s
        ol = s.split('[')
        inte = ol[1].replace(']','')
        if inte in self.inteList:
            self.add('mov r10,[%s]'%inte)
        else:
            self.add('mov r10,%s'%inte)
        return '[%s+8*r10]'%ol[0]
log = glog()

def dealArray(one): 
    one = one.replace(',',' ')
    one = one.replace('|',' ')
    ol = one.split()    
    log.arrayList.append(ol[1])
    if len(ol) == 3:
        log.bAdd(ol[1]+':')
        log.bAdd('resq '+ol[2])
        return
    ss = ''
    for one in ol[3:]:
        ss += one+','
    log.dAdd(ol[1]+':')
    log.dAdd('dq '+ss[:-1])
def dealInte(one):
    one = one.replace(',',' ')
    one = one.replace('|',' ')
    ol = one.split()    
    log.inteList.append(ol[1])
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
    log.add('mov r9,'+log.getToken(ol[2]))
    log.add('mov %s,r9'%log.getToken(ol[1]))
    
def dealAdd(one):
    ol = one.split()
    log.add('mov rax,'+log.getToken(ol[2]))
    log.add('mov r9,'+log.getToken(ol[3]))
    log.add('add rax,r9')
    log.add('mov %s,rax'%log.getToken(ol[1]))
def dealSub(one):
    ol = one.split()
    log.add('mov rax,'+log.getToken(ol[2]))
    log.add('mov r9,'+log.getToken(ol[3]))
    log.add('sub rax,r9')
    log.add('mov %s,rax'%log.getToken(ol[1]))    
def dealMul(one):
    ol = one.split()
    log.add('mov rax,'+log.getToken(ol[2]))
    log.add('mov r9,'+log.getToken(ol[3]))
    log.add('imul r9')
    log.add('mov %s,rax'%log.getToken(ol[1]))  
def dealDiv(one):
    one = one.replace(',',' ')
    ol = one.split()
    log.add('mov rax,'+log.getToken(ol[3]))
    log.add('cmp rax,0')
    la1 = log.getLabel()
    la2 = log.getLabel()
    la3 = log.getLabel()
    log.add('jl '+la1)
    log.add('mov rdx,0')
    log.add('jmp '+la2)
    log.add(la1+':')
    log.add('mov rdx,-1')
    log.add(la2+':')
    log.add('mov r9,'+log.getToken(ol[4]))
    log.add('idiv r9')
    log.add('mov %s,rax'%log.getToken(ol[1]))  
    log.add('mov %s,rdx'%log.getToken(ol[2]))  
    
def dealDef(l):
    one = l[0]
    ol = one.split()
    log.add(ol[1]+':')
    log.add('push r15')
    return l[1:]
def dealWhile(l):
    la = log.getLabel()
    log.add(la+':')
    one = l[0]
    ol = one.split()
    log.add('mov rax,'+log.getToken(ol[1]))
    log.add('mov rcx,'+log.getToken(ol[3]))
    si = ol[2]
    if 'n' in si:
        si = si[1:]
    else:
        si = 'n'+si
    la2 = log.getLabel()
    log.add('cmp rax,rcx')
    log.add('j'+si+' '+la2)
    return la,la2,l[1:]

def dealIf(l):
    one = l[0]
    ol = one.split()
    log.add('mov rax,'+log.getToken(ol[1]))
    log.add('mov rcx,'+log.getToken(ol[3]))
    si = ol[2]
    if 'n' in si:
        si = si[1:]
    else:
        si = 'n'+si
    la = log.getLabel()
    log.add('cmp rax,rcx')
    log.add('j'+si+' '+la)
    return la,l[1:]

def getNextline(l):
    for n in range(len(l)):
        one = l[n]
        two = one.replace(' ','')        
        if two.startswith('#'):
            continue
        two = one.replace(' ','')
        two = two.replace('\n','')
        if not two:
            continue
        return one 
def process(l):
    for n in range(len(l)):
        one = l[n]
        two = one.replace(' ','')        
        if two.startswith('#'):
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
        if ol[0]=='add':
            dealAdd(one)
        if ol[0]=='sub':
            dealSub(one)
        if ol[0]=='mul':
            dealMul(one)
        if ol[0]=='div':
            dealDiv(one)
        if ol[0]=='if':
            return 'dealIf',l[n:]            
        if ol[0]=='continue':
            la,la2 = log.whilecache[-1]
            log.add('jmp '+la)      
        if ol[0]=='break':
            la,la2 = log.whilecache[-1]
            log.add('jmp '+la2)
        if ol[0]=='whileend':
            return 'whileend',l[n+1:]                 
        if ol[0]=='while':
            return 'dealWhile',l[n:]            
        if ol[0]=='def':
            return 'dealDef',l[n:]
        if ol[0]=='defend':
            return 'defend',l[n+1:]
        if ol[0]=='return':
            log.add('pop r15')        
            log.add('ret')
        if ol[0]=='ifend':
            return 'ifend',l[n+1:]     
        if ol[0]=='elseend':
            return 'elseend',l[n+1:]        
        if ol[0]=='call':
            log.add(one)
    return 'end',[]
            

while True:
    a,l = process(l)
    if a=='dealDef':
        l = dealDef(l)
        continue
    if a =='defend':
        log.add('pop r15')
        log.add('ret')
        continue
    if a=='end':
        break
    if a=='dealIf':
        la,l = dealIf(l)
        log.ifcache.append(la)
        continue
    if a=='dealWhile':
        la,la2,l = dealWhile(l)
        log.whilecache.append([la,la2])
        continue
    if a=='whileend':
        la,la2 = log.whilecache.pop()
        log.add('jmp '+la)
        log.add(la2+':')
        continue        
    if a=='elseend':
        la = log.elsecache.pop()
        log.add(la+':')
        continue
    if a=='ifend':
        la = log.ifcache.pop()
        one = getNextline(l)
        if not one:
            continue
        ol = one.split()
        if ol[0] != 'else':
            log.add(la+':')
            continue
        la2 = log.getLabel()
        log.add('jmp '+la2)
        log.add(la+':')
        log.elsecache.append(la2)
        continue
        
ss = log.gen()
f2 = open('out.asm','w')
f2.write(ss)
f2.close()
os.system(' nasm -felf64 out.asm&&gcc out.o -no-pie -o a &&./a ')
