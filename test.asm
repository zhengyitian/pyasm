 global  main
 extern printf
    section .text
    
    main:
    push r15
    mov rcx,[b]
    mov rdx,hehe
mov rax,[hehe+]
   pop r15
    ret 
    section .data
    hehe : dq 1,2,3,4
    b: dq 1
    for1: db "%ld",10,0
    d1: dq 9,-11,1,343,54,6