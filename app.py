import streamlit as st
import os
from assembler import parse_assembly
from riscv_core import RiscVCore
from riscv_defs import ABI_NAMES, ABI_TO_INDEX, disassemble
from instruction_examples import *

# --- 1. SETTINGS & CSS PATH HANDLING ---
st.set_page_config(layout="wide", page_title="RISC-V Sim by Salik")

def load_css(file_name):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(script_directory, file_name)
    try:
        with open(css_path, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception:
        st.sidebar.warning(f"CSS File '{file_name}' not found. UI using default styles.")

load_css("style.css")

# --- 2. DOCUMENTATION & SUMMARIES ---
INSTRUCTION_SUMMARY_MD = """
#### RV32I Base Instruction Set (37 Instructions)
| Instruction Type | Count | Status & Implemented Instructions |
| :--- | :--- | :--- |
| **R-Type** | 10 / 10 | ✅ `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `sra`, `or`, `and` |
| **I-Type** | 9 / 9 | ✅ `addi`, `slti`, `sltiu`, `xori`, `ori`, `andi`, `slli`, `srli`, `srai` |
| **Load** | 5 / 5 | ✅ `lw`, `lb`, `lh`, `lbu`, `lhu` |
| **Store** | 3 / 3 | ✅ `sw`, `sb`, `sh` |
| **Branch** | 6 / 6 | ✅ `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu` |
| **Jump** | 2 / 2 | ✅ `jal`, `jalr` |
| **U-Type**| 2 / 2 | ✅ `lui`, `auipc` |
"""

HELP_DOCUMENTATION_MD = HELP_DOCUMENTATION_MD = """
Welcome to RISC-V Simulator by Salik Javid! This is an interactive tool for writing, assembling, and debugging RV32I assembly code.

**How to Use:**
1.  **Write Code:** Type your RISC-V assembly code in the "Assembly Program" text area below.
2.  **Load an Example:** Alternatively, expand "Show References and Examples" to load a pre-written program.
3.  **Assemble & Load:** Click the `▶️ Assemble & Load` button. This converts your assembly into machine code and loads it into the instruction memory.
4.  **Control Execution:**
    * `⏯️ Step`: Execute one instruction at a time.
    * `⏩ Run to End`: Execute the program until it halts or hits the cycle limit.
    * `🔄 Reset`: Reset the processor and memory to the initial state.

**Understanding the UI:**
* **CPU Registers:** Displays all 32 registers. The border colors group them by their ABI role (e.g., arguments, temporary, saved). Non-zero values are highlighted in green.
* **Instruction Memory:** Shows the assembled machine code. The current instruction pointed to by the Program Counter (PC) is highlighted in yellow.
* **Stack Memory:** This view is centered around the Stack Pointer (SP). The address pointed to by SP is highlighted in orange, making it easy to see stack operations.
* **Data Memory:** A general-purpose memory region for your program's data.
"""

# --- 3. UI HELPER FUNCTIONS ---
def get_reg_group_class(reg_index):
    if reg_index == 0: return ""
    if reg_index in [1, 2, 3, 4]: return "group-special"
    if reg_index in range(5, 8) or reg_index in range(28, 32): return "group-temp"
    if reg_index in range(8, 10) or reg_index in range(18, 28): return "group-saved"
    if reg_index in range(10, 18): return "group-args"
    return ""

def generate_mem_view(title, memory_bytes, start, length, words_per_row=2, highlights=None, layout='row'):
    if highlights is None: highlights = {}
    html = f'<h4>{title}</h4><div class="mem-view">'
    words_in_view = length // 4
    num_rows = (words_in_view + words_per_row - 1) // words_per_row

    for r in range(num_rows):
        html += '<div class="mem-row">'
        for c in range(words_per_row):
            word_index = (c * num_rows + r) if layout == 'col' else (r * words_per_row + c)
            addr = start + word_index * 4
            if word_index >= words_in_view or addr + 4 > len(memory_bytes):
                html += '<div class="mem-word-box empty-box" style="opacity:0.3; border:1px dashed #444;"></div>'
                continue

            val = int.from_bytes(memory_bytes[addr:addr+4], 'little', signed=True)
            hex_val = val & 0xFFFFFFFF
            classes = ["mem-word-box"]
            if val != 0: classes.append("mem-nonzero")
            if addr in highlights: classes.append(highlights[addr])

            is_instr = "Instruction" in title
            disasm = disassemble(hex_val, addr) if is_instr and hex_val != 0 else ""
            sp_label = " &larr; sp" if "sp-highlight" in classes else ""

            html += f'<div class="{" ".join(classes)}">'
            html += f'<span class="mem-addr">0x{addr:03x}:</span> <span class="mem-hex">0x{hex_val:08x}</span>'
            if is_instr: html += f'<span class="mem-disasm">{disasm}</span>'
            else: html += f'<span class="sp-label">{sp_label}</span>'
            html += '</div>'
        html += '</div>'
    return html + '</div>'

# --- 4. LOGIC & STATE MANAGEMENT ---
if 'core' not in st.session_state: st.session_state.core = None
if 'program_info' not in st.session_state: st.session_state.program_info = None
if 'assembly_code' not in st.session_state: st.session_state.assembly_code = "addi t0, x0, 10"

def assemble_and_load():
    try:
        program_info, expansion_log = parse_assembly(st.session_state.assembly_code)
        st.session_state.program_info = {'program': program_info, 'log': expansion_log}
        core = RiscVCore()
        core.load_program(program_info['machine_code'])
        st.session_state.core = core
        st.success("Successfully Assembled!")
    except Exception as e:
        st.error(f"Assembly Error: {e}")
        st.session_state.core = None

# --- 5. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    if st.button("▶️ Assemble & Load", use_container_width=True, type="primary"):
        assemble_and_load()
    
    col1, col2 = st.columns(2)
    if col1.button("⏯️ Step", use_container_width=True, disabled=st.session_state.core is None):
        st.session_state.core.step()
    if col2.button("🔄 Reset", use_container_width=True, disabled=st.session_state.core is None):
        st.session_state.core.reset()
        
    if st.button("⏩ Run to End", use_container_width=True, disabled=st.session_state.core is None):
        st.session_state.core.run()

    st.divider()
    st.subheader("Quick Examples")
    if st.button("Integer (R-Type)", use_container_width=True): st.session_state.assembly_code = R_TYPE_EXAMPLES
    if st.button("Integer (I-Type)", use_container_width=True): st.session_state.assembly_code = I_TYPE_EXAMPLES
    if st.button("Memory Ops", use_container_width=True): st.session_state.assembly_code = MEMORY_EXAMPLES
    if st.button("Branches", use_container_width=True): st.session_state.assembly_code = BRANCH_EXAMPLES_FULL

    if st.button("Jumps & Calls", use_container_width=True): st.session_state.assembly_code = JUMP_CALL_EXAMPLES
    if st.button("Upper Immediate", use_container_width=True): st.session_state.assembly_code = U_TYPE_EXAMPLES
    if st.button("Pseudo-Instructions", use_container_width=True): st.session_state.assembly_code = PSEUDO_INSTRUCTION_EXAMPLES
    
    st.markdown("---")
    with st.popover("📜 Instruction Set Summary", use_container_width=True):
        st.markdown(INSTRUCTION_SUMMARY_MD)

# --- 6. MAIN UI ---
st.title("RISC-V Simulator by Salik Javid")

with st.expander("📖 Quick Help & Documentation"):
    st.markdown(HELP_DOCUMENTATION_MD)

main_col, hardware_col = st.columns([1.2, 1])

with main_col:
    st.subheader("Assembly Editor")
    st.session_state.assembly_code = st.text_area("Write code here:", value=st.session_state.assembly_code, height=400)
    
    if st.session_state.program_info and st.session_state.program_info['log']:
        with st.expander("View Pseudo-Instruction Expansion"):
            st.code('\n'.join(st.session_state.program_info['log']), language='plaintext')

with hardware_col:
    if st.session_state.core:
        core = st.session_state.core
        st.subheader("CPU Registers")
        reg_html = '<div class="reg-container">'
        for i in range(32):
            val = core.regs[i]
            style = f"{get_reg_group_class(i)} {'reg-nonzero' if val != 0 else ''}"
            reg_html += f'<div class="reg-box {style}">{ABI_NAMES[i]} (x{i})<br><b>0x{val & 0xFFFFFFFF:08x}</b></div>'
        st.markdown(reg_html + '</div>', unsafe_allow_html=True)
        
        st.divider()
        mc_len = len(st.session_state.program_info['program']['machine_code']) * 4
        st.markdown(generate_mem_view("Instruction Memory", core.mem, 0, mc_len, words_per_row=1, highlights={core.pc: "pc-highlight"}), unsafe_allow_html=True)
        
        sp_val = core.regs[ABI_TO_INDEX['sp']]
        st.markdown(generate_mem_view("Stack Memory", core.mem, max(0, sp_val-16), 32, words_per_row=1, highlights={sp_val: "sp-highlight"}, layout='col'), unsafe_allow_html=True)
        
        st.markdown(generate_mem_view("Data Memory", core.mem, 512, 64, words_per_row=2), unsafe_allow_html=True)
    else:
        st.info("Assemble & Load a program to see the CPU state.")