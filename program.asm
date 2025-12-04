; Simple LED counter ROM
; Each instruction is 1 byte: [opcode][operand]

; 0x0: A = 0
LDI 0      ; A <- 0
STA F      ; mem[F] <- A

; 0x2: main loop
LDA F      ; A <- mem[F]
OUT        ; show A on LEDs
ADD F      ; A <- A + mem[F]
STA F      ; mem[F] <- A
JMP 2      ; jump back to address 2
HLT        ; not reached, but nice to have
