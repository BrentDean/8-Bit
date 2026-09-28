# Simple 8-bit Instruction Set (Reference)

This document summarizes the instruction set used in Ben Eater’s classic 8-bit breadboard computer project, which my design is loosely based on.

For the original project and videos, see:

- Ben Eater’s 8-bit computer page: https://eater.net/8bit
- CPU control logic and opcodes: https://eater.net/8bit/control

## Overall format

The machine is a very small “SAP-1 style” computer:

- **Data width:** 8 bits
- **Instruction width:** 8 bits
- **Memory / program counter width:** 4 bits (16 addresses total)
- **Instruction format:**  
  - High nibble (bits 7–4): 4-bit opcode  
  - Low nibble (bits 3–0): 4-bit operand (small address or immediate)

Because PC and address buses are only 4 bits wide, the machine can address **16 bytes total**. Instructions and data share this same 16-byte space.

## Instruction set overview

Minimal 4-bit opcode space with 11 defined instructions (the remaining opcode patterns are unused or reserved). A typical mapping is:

| Mnemonic | Opcode (binary) | Meaning                                                           |
|----------|-----------------|-------------------------------------------------------------------|
| `NOP`    | `0000`          | No operation                                                      |
| `LDA`    | `0001`          | Load accumulator from memory address given by low nibble         |
| `ADD`    | `0010`          | Add value at memory address to accumulator                        |
| `SUB`    | `0011`          | Subtract value at memory address from accumulator                 |
| `STA`    | `0100`          | Store accumulator into memory address                             |
| `LDI`    | `0101`          | Load immediate 4-bit value (low nibble) into accumulator          |
| `JMP`    | `0110`          | Unconditional jump to address (low nibble)                        |
| `JC`     | `0111`          | Jump if carry flag is set                                         |
| `JZ`     | `1000`          | Jump if zero flag is set                                          |
| `OUT`    | `1110`          | Copy accumulator to output register (e.g., LEDs)                  |
| `HLT`    | `1111`          | Halt the CPU                                                      |

> Notes:
> - In all memory-access instructions (`LDA`, `ADD`, `SUB`, `STA`), the low nibble is treated as a 4-bit address (0–15).
> - In `LDI`, the low nibble is an immediate literal (0–15) that is zero-extended into the 8-bit accumulator.
> - Jump instructions (`JMP`, `JC`, `JZ`) use the low nibble as an absolute address for the program counter.

## Example machine code

Because each instruction fits in one byte, an 8-bit instruction word looks like:

```text
oooo xxxx
↑↑↑↑ ↑↑↑↑
││││ └┴┴┴── 4-bit operand (address or immediate)
└┴┴┴────── 4-bit opcode
