.section .data
    hello_msg: .asciz "Hello, World!\n"

.section .text
    .global _start

_start:
    // Write 'Hello, World!' to stdout
    mov x0, 1             // File descriptor 1 (stdout)
    ldr x1, =hello_msg    // Pointer to the message
    ldr x2, =13           // Message length
    mov x8, 64            // syscall number for sys_write
    svc 0                 // Call kernel

    // Exit the program
    mov x0, 0             // syscall number for sys_exit
    mov x8, 93            // syscall number for arm64_exit
    svc 0                 // Call kernel
