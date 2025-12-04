# Input File Example (program.asm) :
"""
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
"""


OPCODES = {
    "NOP": 0x00,
    "LDA": 0x10,
    "ADD": 0x20,
    "SUB": 0x30,
    "STA": 0x40,
    "LDI": 0x50,
    "JMP": 0x60,
    "JC":  0x70,
    "JZ":  0x80,
    "OUT": 0xE0,
    "HLT": 0xF0,
}

def encode_line(mnemonic, operand=None):
    base = OPCODES[mnemonic.upper()]
    if operand is None:
        return base
    # 4-bit operand
    return base | (int(operand, 16) & 0x0F)      # HELP - type conversion syntax

program_bytes = []
with open("program.asm") as f:
    for line in f:
        line = line.split(";")[0].strip()  # strip comments
        if not line:
            continue
        parts = line.split()
        if len(parts) == 1:
            program_bytes.append(encode_line(parts[0]))
        else:
            program_bytes.append(encode_line(parts[0], parts[1]))

# write raw bytes to a file
with open("program.bin", "wb") as out:
    out.write(bytes(program_bytes))
    
for b in program_bytes:
    print(f"0x{b:02X}", end=" ")
print()

