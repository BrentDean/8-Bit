# 8-Bit Computer – Hardware + ROM Tooling

> A from-scratch 8-bit CPU, plus Python tools to turn a tiny assembly language into real EEPROM contents.

<img width="1084" height="875" alt="image" src="https://github.com/user-attachments/assets/160945aa-0196-4b6e-9c6c-54597b565c59" />

## Overview

This project is my attempt to connect the “software world” I know (Python, data structures, etc.) with the real hardware that executes instructions.

The goal is to design and build a simple 8-bit CPU on a custom PCB, then write a small toolchain in Python that:

* Assembles a tiny educational ISA into opcodes.
* Packs those opcodes (and eventually microcode) into the correct byte layout for 28C64 EEPROMs.
* Lets me iterate quickly on instruction set design and control logic by just reprogramming ROMs.

The initial ISA and architecture are loosely based on the classic Ben Eater 8-bit breadboard computer, but adapted to a single PCB with updated ICs, and a more explicit software toolchain.

It’s a learning project first: I’m using it to understand what actually happens between “I wrote some code” and “LEDs blink on a real machine.”

## Project Goals

* Build a working 8-bit CPU on a PCB (datapath + control) instead of only in simulation.
* Design a small, clean instruction set that’s easy to reason about and extend.
* Implement a microcoded control unit where `opcode + step + flags → control signals`.
* Write a Python “assembler + ROM image generator” that can:

  * Parse a simple assembly language.
  * Emit the correct bytes for an instruction ROM and/or microcode ROM.
  * Output images suitable for programming a 28C64 EEPROM.
* Use an Arduino Nano running a small C program as a simple EEPROM programmer, so the Python-generated ROM image can be burned directly into a 28C64.

## Hardware Summary

On the hardware side, the design currently includes:

* 8-bit data bus.
* Address bus (sized for 28C64 ROM and external RAM).
* ALU (basic arithmetic and logic).
* General-purpose registers and an accumulator.
* Program counter and instruction register.
* Control logic / microcode ROM.
* RAM and an output register (driving LEDs or similar).

I’m using 28C64 EEPROMs with the extra address lines tied low for now, so the design behaves like a smaller ROM but gives me room to grow later. IC sockets are planned across the board so I can swap ROM contents as I experiment with different programs and microcode layouts.

PCB schematics and layout are done in KiCad; fabrication is in progress.

## Relationship to the Ben Eater 8-bit Computer

This project is inspired by Ben Eater’s 8-bit breadboard computer:

* 8-bit datapath.
* 4-bit opcode + 4-bit operand instruction format.
* Small shared program/data memory.
* Simple accumulator-based design.

The ISA that I’m starting from includes core instructions like:

| Mnemonic | Meaning                                |
| -------- | -------------------------------------- |
| `LDA`    | Load accumulator from memory           |
| `ADD`    | Add memory value to accumulator        |
| `SUB`    | Subtract memory value from accumulator |
| `STA`    | Store accumulator to memory            |
| `LDI`    | Load immediate value into accumulator  |
| `JMP`    | Unconditional jump                     |
| `JC`     | Jump if carry flag set                 |
| `JZ`     | Jump if zero flag set                  |
| `OUT`    | Copy accumulator to output register    |
| `HLT`    | Halt the CPU                           |

My ISA keeps this basic structure and behavior as a starting point, then evolves as I expand the address space, and refine the control logic. A more detailed write-up of how my ISA relates to this “baseline” will live in `docs/ben-eater-isa.md` (work in progress).

## Instruction Set (Work in Progress)

The ISA is intentionally small and educational. Right now I’m experimenting with a 1-byte instruction format:

* High nibble: 4-bit opcode.
* Low nibble: 4-bit operand (immediate or small address).

Example kinds of instructions (subject to change as the hardware evolves):

* `LDI X` – Load immediate value `X` into the accumulator.
* `LDA X` – Load from memory address `X` into the accumulator.
* `STA X` – Store accumulator to memory address `X`.
* `ADD X` – Add value at address `X` to the accumulator.
* `OUT` – Transfer accumulator to the output register.
* `HLT` – Halt.

A tiny sample program in the project’s assembly format might look like:

```asm
; Example: load a value, store it, read it back, and output
LDI 0x0
STA 0xF
LDA 0xF
OUT
HLT
```

The exact mnemonic set and encoding are still being refined; the Python tooling is designed so I can change encodings in one place and regenerate ROM images.

## Microcode & Control ROM

The control unit is microcoded. Conceptually, each clock cycle is defined by a tuple:

```text
(opcode, microstep, flags) → control_word
```

Where:

* `opcode` is the instruction’s high nibble.
* `microstep` is a small counter (T0, T1, T2, …) for each instruction.
* `flags` include things like zero/carry (for conditional jumps later).

The `control_word` is a bitfield that drives signals such as:

* Register load/enable lines.
* ALU operation select lines.
* Memory read/write strobes.
* Program counter increment/load.
* Output register enable.

The long-term plan is to:

1. Define the control word format in a single Python description file.
2. Write microcode “in data” (e.g., tables mapping `(opcode, step, flags)` to control words).
3. Use the same Python tooling to emit a microcode ROM image for a 28C64.

For now, the focus is on assembling regular instructions and getting a basic instruction ROM flowing.

## Python Tooling

The Python side of this repo is a small assembler / ROM image generator. Its responsibilities are:

* Parse a simple assembly source file (e.g., `program.asm`).
* Convert mnemonics + operands into encoded bytes.
* Optionally produce:

  * A human-readable listing (addresses, bytes, decoded instructions).
  * A hex/byte/binary image suitable for EEPROM programming.

Design goals for the tool:

* **Explicit encoding:** All opcode/operand encodings live in one place so they can be changed as the ISA evolves.
* **Deterministic layout:** Address `N` in the generated image always maps to the same place in the ROM and the same cycle in the CPU.
* **Separation of concerns:** Eventually split into:

  * An instruction assembler (for “user programs”).
  * A microcode assembler (for the control ROM).
  * Shared utilities for packing bytes into 28C64-sized images.

Once Python has generated the ROM image, the plan is to hand it off to an **Arduino Nano** running a small C program. The Nano will receive the bytes over serial, drive the address/data lines and write-enable pin on the 28C64, and burn the image directly into the EEPROM.

### How I’m using it right now

Right now the (intended) workflow is intentionally simple:

1. Edit `program.asm` with the instructions I want to test.
2. Run the Python assembler script to:

   * Parse the assembly.
   * Emit a text listing for debugging.
   * Emit a hex/byte/binary image representing the ROM contents.
3. Send that ROM image to an Arduino Nano, which runs a small C program to drive the address/data lines and program the 28C64 EEPROM.
4. Plug the ROM into the CPU board and watch what happens on the LEDs / output register.

As the project stabilizes, I’ll document the exact command-line usage, image format, and Arduino programmer protocol here.

## Status

* ✅ CPU schematic & PCB routed in KiCad.
* ✅ Switched from 28C16 to 28C64 EEPROMs (extra address lines tied low for now).
* ✅ Basic Python assembler & ROM image generator started.
* 🧪 Experimenting with initial ISA and test programs.
* 🔜 Define the control word format and start generating microcode ROM images.
* 🔜 Arduino Nano–based EEPROM programmer in C.
* 🔜 Add hardware photos, block diagrams, and full documentation.

## Learning Focus

Things I’m using this project to learn more deeply:

* How instructions are encoded and fetched on real hardware.
* How microcode sequences control the datapath over multiple cycles.
* How to design a small ISA that’s both workable and teachable.
* How to build simple tooling (assemblers, ROM generators) that mirror what “real” toolchains do, just at 8-bit scale.
* How to connect the software I’m learning (Python, Java, data structures, etc.) directly to observable hardware behavior.

If you’re also into educational CPUs, microcode, or ROM tooling and have suggestions, I’d love to hear them.

## License

License information is still TBD. For now, assume this project is shared for personal and educational use; a formal license will be added once the design stabilizes.
