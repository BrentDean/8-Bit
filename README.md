# 8-Bit Computer — Hardware + ROM Tooling

> A custom-PCB 8-bit CPU project with a Python assembler and an EEPROM programming workflow.

<img width="1084" height="875" alt="8-bit computer project" src="https://github.com/user-attachments/assets/160945aa-0196-4b6e-9c6c-54597b565c59" />

## Overview

This project connects software tooling with the hardware that executes instructions. The design is an educational 8-bit computer adapted from the classic Ben Eater breadboard architecture to a single-PCB layout, with supporting Python tooling for assembling programs into EEPROM-ready bytes.

The repository currently contains:

- exported CPU schematics;
- the current instruction-set reference and sample programs;
- a Python opcode assembler that emits a raw binary image;
- AT28C64/28C16 reference datasheets;
- documentation for the breadboard EEPROM-programmer workflow.

PCB schematic capture and routing were completed in KiCad, and the board was fabricated in December 2025.

## Current implementation

The hardware design includes:

- an 8-bit data bus;
- an accumulator and general-purpose registers;
- an ALU for arithmetic and logic operations;
- a program counter and instruction register;
- RAM and an output register;
- microcoded control logic;
- AT28C64 EEPROMs, currently used with the additional address lines tied low for the 4-bit address mode.

The current software assembler parses the project's assembly syntax, converts mnemonics and operands into one-byte instructions, writes the result to `program.bin`, and prints the encoded bytes for inspection.

A breadboard EEPROM-programmer proof of concept has also been built around an Arduino Nano, 74HC595 shift registers, and a ZIF socket.

## Instruction set

The current assembler uses a one-byte instruction format:

- high nibble: 4-bit opcode;
- low nibble: 4-bit operand, used as an address or immediate value.

| Mnemonic | Meaning |
| --- | --- |
| `NOP` | No operation |
| `LDA` | Load accumulator from memory |
| `ADD` | Add memory value to accumulator |
| `SUB` | Subtract memory value from accumulator |
| `STA` | Store accumulator to memory |
| `LDI` | Load immediate value |
| `JMP` | Unconditional jump |
| `JC` | Jump if carry is set |
| `JZ` | Jump if zero is set |
| `OUT` | Copy accumulator to output register |
| `HLT` | Halt |

Example:

```asm
LDI 0
STA F
LDA F
OUT
HLT
```

The current encoding is intentionally small and easy to inspect. The Python implementation keeps opcode definitions in one place so the instruction mapping can be revised as the hardware evolves.

## Python assembler

The assembler lives under `software/assembler/`.

Its current responsibilities are deliberately narrow:

1. read `program.asm`;
2. remove comments and blank lines;
3. encode mnemonics and hexadecimal operands;
4. write the resulting bytes to `program.bin`;
5. print the encoded bytes for verification.

The repository also includes example assembly and generated hexadecimal output for the current instruction set.

Microcode-image generation is a planned extension rather than a capability claimed by the current assembler.

## Control architecture

The CPU uses a microcoded control model. Conceptually, execution maps:

```text
(opcode, microstep, flags) → control signals
```

The control signals drive operations such as register load/enable lines, ALU selection, memory access, program-counter control, and output-register updates.

The next control-unit tooling step is to represent those sequences as data and generate control-ROM images from the same Python-based workflow.

## EEPROM programmer

The EEPROM-programmer prototype uses:

- an Arduino Nano;
- 74HC595 shift registers;
- a ZIF socket;
- an AT28C64 EEPROM.

For each write, the programmer presents an address and data byte, controls `/CE`, `/OE`, and `/WE`, waits for the write cycle, and can read the value back for verification.

![Breadboard EEPROM programmer](https://github.com/user-attachments/assets/ed122e92-34ca-4568-861b-e0bb1d2ac3df)

The intended end-to-end workflow is:

1. edit an assembly program;
2. generate the ROM bytes with the Python assembler;
3. transfer the bytes to the EEPROM-programmer workflow;
4. program and verify the AT28C64;
5. install the EEPROM in the CPU board and observe the program on the hardware.

The breadboard programmer is the current hardware proof of concept; tighter software/firmware integration remains part of the project roadmap.

## Project status

### Completed

- CPU schematic and PCB routing in KiCad.
- PCB fabrication.
- Required component sourcing.
- Migration from 28C16 to AT28C64 EEPROMs.
- Breadboard EEPROM-programmer proof of concept.
- Initial Python opcode assembler and sample programs.
- Exported module schematics and ISA documentation.

### Active development

- PCB assembly and electrical bring-up.
- ISA refinement and hardware test programs.

### Planned extensions

- Define the control-word format in code.
- Generate microcode/control-ROM images.
- Complete the integrated Arduino programming workflow.
- Add further hardware bring-up evidence and documentation.

![First batch of ICs and components](https://github.com/user-attachments/assets/fbcfeaa9-a79d-4684-85a2-baaf29e83c57)

## Repository layout

```text
datasheets/                 EEPROM reference datasheets
hardware/schematics/        Exported CPU and module schematics
software/assembler/         Python assembler and ISA reference
software/examples/          Example assembly and generated output
ISA-Reference.md            Current ISA reference
ISA.txt                     Example ROM-address / byte mapping
```

## Learning focus

This project is primarily an exercise in:

- CPU datapaths, registers, buses, ALUs, flags, and control sequencing;
- digital logic and timing;
- schematic capture, PCB layout, and manufacturability;
- EEPROM programming and component-level interfaces;
- instruction encoding and microcode;
- connecting Python tooling to observable hardware behavior.

## Acknowledgements

- [Ben Eater's 8-bit computer](https://eater.net/8bit) provided the original SAP-style architecture and instruction format that this project builds on. The EEPROM and microcode approach was also informed by his [Arduino EEPROM programmer](https://www.youtube.com/watch?v=K88pgWhEb1M) material.
- The single-board layout was influenced by the PCB work of [The-Invent0r](https://github.com/The-Invent0r/).

This project is an independent, non-affiliated derivative work.
