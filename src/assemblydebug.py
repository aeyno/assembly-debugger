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


prog_name = "a.out"
if len(sys.argv) > 1:
    prog_name = sys.argv[-1]

dbg = lldb.SBDebugger().Create()
dbg.SetAsync (False)

print(f"Debugging {prog_name}")
target : SBTarget = dbg.CreateTarget(prog_name)

if target:
    # bp = target.EvaluateExpression("break set -p return -X main")
    #bp = target.BreakpointCreateByLocation("main.c", 7)
    # bp = target.BreakpointCreateByRegex("return")
    strlist = SBStringList()
    strlist.AppendString("main")
    # bp = target.BreakpointCreateBySourceRegex("return", SBFileSpecList(), SBFileSpecList(), strlist)
    # bp = target.BreakpointCreateByName("breakpoint")
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

        registerList = frame.GetRegisters()
        print('Frame registers (size of register set = %d):' % registerList.GetSize())
        # for value in registerList:
        #     print_registers(value)
        print("\n>>>>>>> REGISTERS DUMP <<<<<<<<")
        print_registers(registerList[0]) # Registres generaux
        process.Continue()
        
        print("\n>>>>>>> STDOUT <<<<<<<<")
        mystr = process.GetSTDOUT(100000)
        print(mystr)

# val3 = target.EvaluateExpression("register read --format u")
