#!/bin/python3
import sys
import os
import lldb
from lldb import SBTarget, SBValue, SBStringList, SBFileSpecList, SBProcess


def print_registers(register_set):
    print('%s (number of children = %d):' % (register_set.GetName(), register_set.GetNumChildren()))
    child: SBValue
    for child in register_set:
        print('\tName: ', child.GetName(), ' Value: ', child.GetValue())
    

if __name__ == "__main__":
    prog_name = "a.out"
    if len(sys.argv) > 1:
        prog_name = sys.argv[-1]

    
    dbg = lldb.SBDebugger().Create()
    dbg.SetAsync (False)
    target : SBTarget = dbg.CreateTarget(prog_name)

    if not target:
        print(f"'{prog_name}' not found.")
        exit(1)

    print("\n>>>>>>> SETTING BREAKPOINT <<<<<<<<")
    bp = target.BreakpointCreateByRegex("breakpoint")
    print(f"breakpoint : {bp}")

    process : SBProcess = target.LaunchSimple (None, None, os.getcwd())
    bp_counter = 1
    while process.is_alive:
        print(f"\n>>>>>>> BREAKPOINT {bp_counter} <<<<<<<<")
        bp_counter += 1
        print(f"process: {process}")

        thread = process.GetThreadAtIndex (0)
        print(f"thread: {thread}")

        frame = thread.GetFrameAtIndex (0)
        print(f"frame: {frame}")

        
        print("\n>>>>>>> REGISTERS DUMP <<<<<<<<")

        registerList = frame.GetRegisters()
        print('Frame registers (size of register set = %d):' % registerList.GetSize())
        # for value in registerList:
        #     print_registers(value)
        # Printing General Purpose Registers
        print_registers(registerList[0])
        process.Continue()
        
        print("\n>>>>>>> STDOUT <<<<<<<<")
        stdout_data = process.GetSTDOUT(100000)
        print(stdout_data)