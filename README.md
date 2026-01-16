# RISC-V (RV32I) Processor Simulator

<div align="center">
  <img src="/images/RISC-V-logo.svg.png" alt="RISC-V Simulator Title" width="800"/>

</div>

---

## Table of Contents

- [Introduction](#introduction)
- [What is RISC-V?](#what-is-risc-v)
- [What is a Processor Simulator?](#what-is-a-processor-simulator)
- [Project Overview](#project-overview)
- [Architecture Basics](#architecture-basics)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Supported Instructions](#supported-instructions)
- [Usage Examples](#usage-examples)
- [Understanding the Code](#understanding-the-code)
- [Contributing](#contributing)
- [Resources](#resources)

---

## Introduction

Welcome to the **RISC-V (RV32I) Processor Simulator**! This project is a Python-based simulator that emulates a RISC-V 32-bit integer processor. Whether you're a student learning computer architecture, a developer exploring RISC-V, or simply curious about how processors work, this simulator will help you understand the fundamentals.

### What You'll Learn

- How processors execute instructions
- The RISC-V instruction set architecture (ISA)
- Binary encoding and decoding
- Register operations and memory management
- The fetch-decode-execute cycle

---

## What is RISC-V?

**RISC-V** (pronounced "risk five") is an **open-source instruction set architecture (ISA)**. Think of it as the "language" that a processor understands.

### Key Characteristics

- **RISC** = Reduced Instruction Set Computer

  - Uses a small, simple set of instructions
  - Each instruction does one simple thing
  - Easier to learn and implement than complex ISAs

- **Open Source & Free**

  - Unlike ARM or x86 (Intel/AMD), RISC-V is not owned by any company
  - Anyone can design and build RISC-V processors
  - No licensing fees or restrictions

- **Modular Design**
  - Base instruction set: RV32I (32-bit integers)
  - Optional extensions: M (multiply/divide), A (atomic), F (floating-point), etc.

### Why RISC-V?

- **Educational**: Clean, well-documented design perfect for learning
- **Growing**: Used in everything from embedded systems to supercomputers
- **Future-proof**: Industry adoption is rapidly increasing

---

## 💻 What is a Processor Simulator?

A **processor simulator** (also called an **emulator** or **interpreter**) is a program that mimics how a real processor works, but runs in software instead of hardware.

### Real Processor vs. Simulator

| Real Processor            | Our Simulator           |
| ------------------------- | ----------------------- |
| Hardware circuits         | Python code             |
| Executes at GHz speeds    | Executes step-by-step   |
| Processes binary directly | Interprets instructions |
| Fixed after manufacturing | Can be modified easily  |

### Benefits of Using a Simulator

✅ **Learning**: See exactly what happens at each step  
✅ **Debugging**: Inspect registers and memory at any time  
✅ **Experimentation**: Try different programs safely  
✅ **No Hardware Needed**: Runs on any computer with Python

---

## Project Overview

This simulator implements the **RV32I** base integer instruction set, which includes:

- **32 general-purpose registers** (x0 to x31)
- **Arithmetic operations** (ADD, SUB, ADDI, etc.)
- **Logical operations** (AND, OR, XOR, etc.)
- **Shift operations** (SLL, SRL, SRA, etc.)
- **Memory operations** (Load/Store - future implementation)
- **Control flow** (Branches, Jumps - future implementation)

### What This Simulator Does

1. **Loads** machine code instructions
2. **Decodes** them to understand what operation to perform
3. **Executes** the operation (modifies registers/memory)
4. **Tracks** changes for visualization
5. **Repeats** until the program ends

---

## Architecture Basics

### The Processor Components

```
┌─────────────────────────────────────┐
│      RISC-V RV32I Processor         │
│                                     │
│  ┌───────────────────────────┐      │
│  │   Register File (32 regs) │      │
│  │   x0 = 0 (hardwired)      │      │
│  │   x1, x2, ..., x31        │      │
│  └───────────────────────────┘      │
│                                     │
│  ┌───────────────────────────┐      │
│  │   Program Counter (PC)    │      │
│  │   Points to next instr.   │      │
│  └───────────────────────────┘      │
│                                     │
│  ┌───────────────────────────┐      │
│  │   Memory (RAM)            │      │
│  │   Stores data & programs  │      │
│  └───────────────────────────┘      │
│                                     │
│  ┌───────────────────────────┐      │
│  │   Instruction Decoder     │      │
│  │   Interprets binary       │      │
│  └───────────────────────────┘      │
│                                     │
│  ┌───────────────────────────┐      │
│  │   ALU (Arithmetic Logic)  │      │
│  │   Performs operations     │      │
│  └───────────────────────────┘      │
└─────────────────────────────────────┘
```

### Key Concepts

#### 1. **Registers**

- **What**: Super-fast storage locations inside the CPU
- **How many**: 32 registers (x0 to x31)
- **Size**: Each holds 32 bits (4 bytes)
- **Special**: x0 is always 0 (cannot be changed)

#### 2. **Program Counter (PC)**

- **What**: Keeps track of which instruction to execute next
- **How**: Stores the memory address of the current instruction
- **Updates**: Increments by 4 after each instruction (each instruction is 4 bytes)

#### 3. **Memory**

- **What**: Storage for programs and data
- **Organization**: Byte-addressable (each byte has an address)
- **In our simulator**: Implemented as a Python dictionary

#### 4. **Instructions**

- **What**: Commands that tell the processor what to do
- **Format**: 32-bit binary numbers with encoded information
- **Example**: `0x003100B3` = ADD x1, x2, x3

### The Fetch-Decode-Execute Cycle

This is the **heartbeat** of any processor:

```
   ┌─────────┐
   │ FETCH   │  Get instruction from memory at PC
   └────┬────┘
        │
   ┌────▼────┐
   │ DECODE  │  Figure out what instruction it is
   └────┬────┘
        │
   ┌────▼────┐
   │ EXECUTE │  Perform the operation
   └────┬────┘
        │
   ┌────▼────┐
   │ UPDATE  │  PC = PC + 4
   └────┬────┘
        │
        └─────► Repeat
```

**Example:**

```
PC = 0: Fetch instruction at address 0
        Decode: It's ADD x3, x1, x2
        Execute: x3 = x1 + x2
        Update: PC = 4

PC = 4: Fetch instruction at address 4
        ... and so on
```

---

## Prerequisites

Before running this simulator, you should have:

### Required Knowledge

- **Basic Python**: Variables, functions, classes
- **Binary/Hexadecimal**: Understanding of number systems
  - Binary: `0b10101010`
  - Hexadecimal: `0xFF`
- **Bitwise Operations**: `&`, `|`, `^`, `<<`, `>>`

### Nice to Have (But Not Required)

- Basic understanding of computer architecture
- Familiarity with assembly language concepts

### System Requirements

- Python 3.7 or higher
- Any operating system (Windows, macOS, Linux)
- Text editor or IDE (VS Code, PyCharm, etc.)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/SALIK-JAVID/RISC-V-Simulator.git
cd risc-v-simulator
```

### Step 2: Set Up Virtual Environment

A virtual environment keeps your project dependencies isolated.

#### On Linux/macOS:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### On Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**You'll know it's activated when you see `(venv)` in your terminal prompt:**

```bash
(venv) user@computer:~/risc-v-simulator$
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet, you can create it:

```bash
# For basic simulator (no dependencies yet)
# Future: streamlit, pytest, etc.
```

---

## 📁 Project Structure

```
risc-v-simulator/
│
├── venv/                    # Virtual environment (created by you)
│
├── images/                  # Project images
│
│
├── riscv_defs.py           # RISC-V architectural definitions
│   ├── Opcodes
│   ├── Funct3/Funct7 codes
│   ├── Register names
│   └── Helper functions
│
├── riscv_core.py           # Core processor simulator logic
│   ├── RiscVProcessor class
│   ├── Register operations
│   ├── Instruction decoding
│   └── Execution methods
│
├── assembler.py            # (Future) Assembly to machine code
│
├── app.py                  # (Future) Streamlit web interface
│
├── instruction_examples.py # (Future) Example programs
│
├── test_simulator.py       # Unit tests
│
│
└── README.md              # This file!
```

### File Descriptions

#### `riscv_defs.py`

Contains all the constants and definitions for RV32I:

- Opcodes (identify instruction types)
- Funct3/Funct7 codes (specify exact operations)
- Register name mappings (t0 → x5, a0 → x10)
- Bit masks and positions
- Helper functions (sign extension, etc.)

#### `riscv_core.py`

The main processor simulator:

- `RiscVProcessor` class
- Register file (32 registers)
- Memory (dictionary-based)
- Instruction decoder
- Execution methods for each instruction
- Fetch-decode-execute cycle

---

## ⚙️ How It Works

### Instruction Encoding

Every RISC-V instruction is a **32-bit binary number** with encoded fields.

#### Example: ADD Instruction

```assembly
ADD x3, x1, x2    # x3 = x1 + x2
```

**Binary encoding:**

```
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ funct7  │   rs2   │   rs1   │ funct3  │   rd    │ opcode  │
│ [31:25] │ [24:20] │ [19:15] │ [14:12] │ [11:7]  │  [6:0]  │
├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ 0000000 │  00010  │  00001  │   000   │  00011  │ 0110011 │
│    0    │    2    │    1    │    0    │    3    │  0x33   │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

Hexadecimal: 0x003100B3
```

**Field meanings:**

- **opcode (0x33)**: R-type arithmetic instruction
- **rd (3)**: Destination register = x3
- **funct3 (0)**: Could be ADD or SUB
- **rs1 (1)**: First source register = x1
- **rs2 (2)**: Second source register = x2
- **funct7 (0)**: Specifies ADD (not SUB)

### Instruction Types

RISC-V has 6 instruction formats:

#### 1. **R-Type** (Register-Register)

```
Format: funct7 | rs2 | rs1 | funct3 | rd | opcode
Example: ADD x1, x2, x3
```

#### 2. **I-Type** (Immediate)

```
Format: imm[11:0] | rs1 | funct3 | rd | opcode
Example: ADDI x1, x2, 100
```

#### 3. **S-Type** (Store)

```
Format: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
Example: SW x1, 4(x2)
```

#### 4. **B-Type** (Branch)

```
Format: imm[12|10:5] | rs2 | rs1 | funct3 | imm[4:1|11] | opcode
Example: BEQ x1, x2, label
```

#### 5. **U-Type** (Upper Immediate)

```
Format: imm[31:12] | rd | opcode
Example: LUI x1, 0x12345
```

#### 6. **J-Type** (Jump)

```
Format: imm[20|10:1|11|19:12] | rd | opcode
Example: JAL x1, label
```

### Decoding Process

```python
# Step 1: Extract opcode
opcode = instruction & 0x7F  # Last 7 bits

# Step 2: Determine instruction type
if opcode == 0x33:  # R-type
    # Extract R-type fields
    rd = (instruction >> 7) & 0x1F
    funct3 = (instruction >> 12) & 0x7
    rs1 = (instruction >> 15) & 0x1F
    rs2 = (instruction >> 20) & 0x1F
    funct7 = (instruction >> 25) & 0x7F

# Step 3: Determine exact operation
if funct3 == 0x0 and funct7 == 0x00:
    # This is ADD
    execute_add(rs1, rs2, rd)
```

---

## 📖 Supported Instructions

### Currently Implemented

#### Arithmetic (R-Type & I-Type)

| Instruction | Format       | Operation      | Description        |
| ----------- | ------------ | -------------- | ------------------ |
| `ADD`       | rd, rs1, rs2 | rd = rs1 + rs2 | Add two registers  |
| `SUB`       | rd, rs1, rs2 | rd = rs1 - rs2 | Subtract registers |
| `ADDI`      | rd, rs1, imm | rd = rs1 + imm | Add immediate      |

#### Logical (R-Type & I-Type)

| Instruction | Format       | Operation       | Description   |
| ----------- | ------------ | --------------- | ------------- |
| `AND`       | rd, rs1, rs2 | rd = rs1 & rs2  | Bitwise AND   |
| `OR`        | rd, rs1, rs2 | rd = rs1 \| rs2 | Bitwise OR    |
| `XOR`       | rd, rs1, rs2 | rd = rs1 ^ rs2  | Bitwise XOR   |
| `ANDI`      | rd, rs1, imm | rd = rs1 & imm  | AND immediate |
| `ORI`       | rd, rs1, imm | rd = rs1 \| imm | OR immediate  |
| `XORI`      | rd, rs1, imm | rd = rs1 ^ imm  | XOR immediate |

#### Shift (R-Type & I-Type)

| Instruction | Format       | Operation       | Description             |
| ----------- | ------------ | --------------- | ----------------------- |
| `SLL`       | rd, rs1, rs2 | rd = rs1 << rs2 | Shift left logical      |
| `SRL`       | rd, rs1, rs2 | rd = rs1 >> rs2 | Shift right logical     |
| `SRA`       | rd, rs1, rs2 | rd = rs1 >> rs2 | Shift right arithmetic  |
| `SLLI`      | rd, rs1, imm | rd = rs1 << imm | Shift left immediate    |
| `SRLI`      | rd, rs1, imm | rd = rs1 >> imm | Shift right immediate   |
| `SRAI`      | rd, rs1, imm | rd = rs1 >> imm | Shift right arith. imm. |

### Register Names (ABI)

| Register | ABI Name | Description        | Saved? |
| -------- | -------- | ------------------ | ------ |
| x0       | zero     | Hardwired zero     | N/A    |
| x1       | ra       | Return address     | No     |
| x2       | sp       | Stack pointer      | Yes    |
| x3       | gp       | Global pointer     | -      |
| x4       | tp       | Thread pointer     | -      |
| x5-x7    | t0-t2    | Temporaries        | No     |
| x8-x9    | s0-s1    | Saved registers    | Yes    |
| x10-x17  | a0-a7    | Function arguments | No     |
| x18-x27  | s2-s11   | Saved registers    | Yes    |
| x28-x31  | t3-t6    | Temporaries        | No     |

---

## Usage Examples

### Example 1: Basic Arithmetic

```python
from riscv_core import RiscVProcessor

# Create processor
cpu = RiscVProcessor()

# Program: Add two numbers
# ADDI x1, x0, 5   # x1 = 5
# ADDI x2, x0, 10  # x2 = 10
# ADD x3, x1, x2   # x3 = x1 + x2 = 15

instructions = [
    0x00500093,  # ADDI x1, x0, 5
    0x00A00113,  # ADDI x2, x0, 10
    0x002081B3,  # ADD x3, x1, x2
]

# Load and run
cpu.load_program(instructions)
cpu.run()

# Check results
print(f"x1 = {cpu.registers[1]}")  # Output: x1 = 5
print(f"x2 = {cpu.registers[2]}")  # Output: x2 = 10
print(f"x3 = {cpu.registers[3]}")  # Output: x3 = 15
```

### Example 2: Logical Operations

```python
# Program: Bitwise operations
# ADDI x1, x0, 0xFF    # x1 = 255
# ADDI x2, x0, 0x0F    # x2 = 15
# AND x3, x1, x2       # x3 = 255 & 15 = 15
# OR x4, x1, x2        # x4 = 255 | 15 = 255
# XOR x5, x1, x2       # x5 = 255 ^ 15 = 240

instructions = [
    0x0FF00093,  # ADDI x1, x0, 255
    0x00F00113,  # ADDI x2, x0, 15
    0x002571B3,  # AND x3, x1, x2
    0x00256233,  # OR x4, x1, x2
    0x002542B3,  # XOR x5, x1, x2
]

cpu.load_program(instructions)
cpu.run()

print(f"x3 (AND) = {cpu.registers[3]}")  # Output: 15
print(f"x4 (OR) = {cpu.registers[4]}")   # Output: 255
print(f"x5 (XOR) = {cpu.registers[5]}")  # Output: 240
```

### Example 3: Shift Operations

```python
# Program: Multiply by 4 using shift
# ADDI x1, x0, 8       # x1 = 8
# SLLI x2, x1, 2       # x2 = x1 << 2 = 8 * 4 = 32

instructions = [
    0x00800093,  # ADDI x1, x0, 8
    0x00209113,  # SLLI x2, x1, 2
]

cpu.load_program(instructions)
cpu.run()

print(f"x1 = {cpu.registers[1]}")  # Output: 8
print(f"x2 = {cpu.registers[2]}")  # Output: 32
```

### Example 4: Step-by-Step Execution

```python
# Load program
cpu.load_program(instructions)

# Execute step by step
while cpu.step():
    print(f"PC = {cpu.pc}, x1 = {cpu.registers[1]}, x2 = {cpu.registers[2]}")

# Output:
# PC = 4, x1 = 5, x2 = 0
# PC = 8, x1 = 5, x2 = 10
# PC = 12, x1 = 5, x2 = 10
```

---

## 🔍 Understanding the Code

### Key Concepts in Python

#### 1. Bitwise Operations

```python
# AND (&) - Keep bits where both are 1
0b1100 & 0b1010 = 0b1000  # 12 & 10 = 8

# OR (|) - Keep bits where either is 1
0b1100 | 0b1010 = 0b1110  # 12 | 10 = 14

# XOR (^) - Keep bits where exactly one is 1
0b1100 ^ 0b1010 = 0b0110  # 12 ^ 10 = 6

# Left Shift (<<) - Multiply by 2^n
0b0101 << 2 = 0b10100  # 5 << 2 = 20

# Right Shift (>>) - Divide by 2^n
0b10100 >> 2 = 0b0101  # 20 >> 2 = 5
```

#### 2. Extracting Bit Fields

```python
instruction = 0x003100B3

# Extract bits [11:7] (rd field)
rd = (instruction >> 7) & 0x1F
#     ^^^^^^^^^^^^^^^^   ^^^^^^
#     Shift right 7      Mask to 5 bits (0b11111)

# Step by step:
# instruction = 0x003100B3 = 0b00000000001100010000000010110011
# instruction >> 7 =         0b00000000000001100010000000001
# result & 0x1F =            0b00011 = 3 (x3)
```

#### 3. Sign Extension

```python
def sign_extend(value, bits):
    """Extend a signed number from 'bits' to 32 bits"""
    sign_bit = 1 << (bits - 1)
    if value & sign_bit:  # Negative number
        # Extend with 1s
        mask = (1 << bits) - 1
        return value | (~mask & 0xFFFFFFFF)
    else:
        return value

# Example:
sign_extend(0x800, 12)  # 0x800 = -2048 in 12 bits
# Result: 0xFFFFF800 = -2048 in 32 bits
```

### Understanding the Processor Class

```python
class RiscVProcessor:
    def __init__(self):
        # 32 registers, all zeros
        self.registers = [0] * 32

        # Memory (dictionary for sparse allocation)
        self.memory = {}

        # Program counter
        self.pc = 0

    def write_register(self, rd, value):
        if rd != 0:  # x0 is hardwired to 0
            self.registers[rd] = value & 0xFFFFFFFF

    def execute_add(self, rs1, rs2, rd):
        result = self.registers[rs1] + self.registers[rs2]
        self.write_register(rd, result)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Reporting Issues

Found a bug? Have a suggestion?

- Open an issue on GitHub
- Provide clear description and steps to reproduce
- Include Python version and OS

---

## Resources

### RISC-V Documentation

- [RISC-V Official Website](https://riscv.org)
- [RISC-V Specifications](https://riscv.org/technical/specifications/)
- [RISC-V Reader (Free Book)](http://www.riscvbook.com/)
- [RISC-V Green Card (Reference)](https://www.cl.cam.ac.uk/teaching/1617/ECAD+Arch/files/docs/RISCVGreenCardv8-20151013.pdf)

### Learning Materials

- [Computer Organization and Design: RISC-V Edition](https://www.amazon.com/Computer-Organization-Design-RISC-V-Architecture/dp/0128122757)
- [RISC-V Assembly Programming Tutorial](https://www.youtube.com/watch?v=YuYJzMEQljg)
- [Digital Design & Computer Architecture: RISC-V Edition](https://www.amazon.com/Digital-Design-Computer-Architecture-RISC-V/dp/0128200642)

### Online Tools

- [RISC-V Online Simulator](https://www.cs.cornell.edu/courses/cs3410/2019sp/riscv/interpreter/)
- [Venus RISC-V Simulator](https://venus.cs61c.org/)
- [RISC-V Assembler](https://riscvasm.lucasteske.dev/)

### Python Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Python Bitwise Operations](https://realpython.com/python-bitwise-operators/)
- [Object-Oriented Programming in Python](https://realpython.com/python3-object-oriented-programming/)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**SALIK-JAVID**

- GitHub: [@SALIK-JAVID](https://github.com/SALIK-JAVID)
- Email: salikjaveeddar@gmail.com

---

## Acknowledgments

- RISC-V Foundation for the open ISA specification
- Computer architecture textbooks and courses
- The open-source community

---

## Support

Need help? Have questions?

- 📧 Email: salikjaveeddar@gmail.com

---

<div align="center">
  <p>Made with ❤️ for learning and education</p>
  <p>⭐ Star this repo if you find it helpful!</p>
</div>

---

## 🎯 Quick Start Summary

```bash
# 1. Clone repository
git clone https://github.com/SALIK-JAVID/RISC-V-Simulator.git
cd risc-v-simulator

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install streamlit


# 4. Try the simulator
python
>>>  streamlit run app.py
>>> # Start coding!
```

**Happy Learning! 🚀**
