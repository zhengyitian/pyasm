 global  main
 extern printf
    section .text
    
    main:
    push r15
mov rdi,for1
mov rsi,10
mov rax ,0
call printf
mov rdx,-1
mov rax,-1000
mov rcx,3
idiv rcx
mov rsi,rdx
mov rdi,for1
mov rax ,0
call printf

   pop r15
    ret 
    section .data
    hehe : dq 1,2,3,4
    b: dq 1
    for1: db "%ld",10,0
    d1: dq 9,-11,1,343,54,6