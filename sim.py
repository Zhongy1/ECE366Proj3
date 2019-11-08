# ECE 366 Project 3 Fall 2019
# Group 12: Zhongyi Chen & Claire Chappee
f = 0;
instr_logging = True

registers = {
    '00': 0,
    '01': 0,
    '10': 0,
    '11': 0,
    'pc': 0
}
register_names = {
    '00': '$0',
    '01': '$1',
    '10': '$2',
    '11': '$3',
    'pc': 'pc'
}

# 2^9 needs to be the size of our memory
memory = [0] * 512
instr_memory = []

def executeLine(line):
    if(line[0:2] == "00"): #lui
        rx = line[2:4]
        imm = int(line[4:8], 2)
        immExt = imm << 4
        registers[rx] = immExt
        registers['pc'] += 1
        if (instr_logging == True):
            f.write("Instruction: lui " + register_names[rx] + ", " + str(imm) + '\n')
            f.write("Register[" + register_names[rx] + "] now has value " + str(registers[rx]) + "\n")
            f.write("PC is now: " + str(registers['pc']) + "\n")

    if(line[0:2] == "01"): #addi
        rx = line[2:4]
        imm = int(line[4:8], 2)
        registers[rx] = registers[rx] + imm
        registers['pc'] += 1
        if (instr_logging == True):
            f.write("Instruction: addi " + register_names[rx] + ", " + str(imm) + "\n")
            f.write("Register[" + register_names[rx] + "] now has value " + str(registers[rx]) + "\n")
            f.write("PC is now: " + str(registers['pc']) + "\n")

    if(line[0:2] == "10"): #hash 
        rx = line[2:4]
        ry = line[4:6]
        rz = line[6:8]
        #registers[rx] = H(ry, rz)
        srcA = registers[ry]
        srcB = registers[rz]
        for i in range(0, 5):
            product = srcA * srcB
            hi = (product & 0xFF00) >> 8
            lo = product & 0xFF
            srcA = hi ^ lo
        srcB = srcA & 0xF
        srcA = (srcA & 0xF0) >> 4
        c = srcA ^ srcB
        registers[rx] = ((c & 0xC) >> 2) ^ (c & 0x3)
        registers['pc'] += 1
        if (instr_logging == True):
            f.write("Instruction: hash " + register_names[rx] + ", " + register_names[ry] + ", " + register_names[rz] + "\n")
            f.write("Register[" + register_names[rx] + "] now has value " + str(registers[rx]) + "\n")
            f.write("PC is now: " + str(registers['pc']) + "\n")

    if(line[0:4] == "1100"): #ldinc
        rx = line[4:6]
        ry = line[6:8]
        registers[rx] = memory[registers[ry]] + 1
        registers['pc'] += 1
        if (instr_logging == True):
            f.write("Instruction: ldinc " + register_names[rx] + ", " + "(" + register_names[ry] + ")\n")
            f.write("Register[" + register_names[rx] + "] now has value " + str(registers[rx]) + "\n")
            f.write("PC is now: " + str(registers['pc']) + "\n")

    if(line[0:4] == "1110"): #st 
        rx = line[4:6]
        ry = line[6:8]
        memory[registers[ry]] = registers[rx]
        registers['pc'] += 1
        if (instr_logging == True):
            f.write("Instruction: st " + register_names[rx] + ", " + "(" + register_names[ry] + ")\n" )
            f.write("Register[" + register_names[rx] + "] now has value " + str(registers[rx]) + "\n")
            f.write("PC is now: " + str(registers['pc']) + "\n")

    if(line[0:4] == "1111"): #sto3inc 
        rx = line[4:6]
        ry = line[6:8]
        memory[registers[ry] + 3] = registers[rx]
        registers[ry] += 1
        registers['pc'] += 1
        if (instr_logging == True):
            f.write("Instruction: sto3inc " + register_names[rx] + ", " + "(" + register_names[ry] + ")\n" )
            f.write("Register[" + register_names[rx] + "] now has value " + str(registers[rx]) + "\n")
            f.write("PC is now: " + str(registers['pc']) + "\n")

def initializeInstrMemory(instr_mem_array, mCode):
    for line in mCode:
        line = line.strip()
        if (line == ''):
            continue
        else:
            instr_mem_array.append(line)

def main():
    global f
    global registers
    global register_names
    global memory
    global instr_memory

    f1 = open("outputFA.txt","w+")
    h1 = open("mc1.txt","r")
    f2 = open("output19.txt","w+")
    h2 = open("mc2.txt","r")
    f3 = open("outputE3.txt","w+")
    h3 = open("mc3.txt","r")
    f4 = open("output66.txt","w+")
    h4 = open("mc4.txt","r")

    if (instr_logging == True):
        f = f1
    mCode = h1.readlines() 
    initializeInstrMemory(instr_memory, mCode)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] < instrCount):
        mcLine = instr_memory[registers['pc']]
        executeLine(mcLine)
        dynamInstrCount += 1
    #Output for B = FA
    f1.write('\nECE 366 Project 3\n')
    f1.write('Created by: Zhongy Chen and Claire Chappee\n')
    f1.write('Final Output for mc1.txt\n')
    f1.write('****************************************************\n')
    f1.write('Registers and their value\n')
    for key in registers:
        f1.write(register_names[key] + ' --> ' + str(registers[key]) + '\n')
    f1.write('****************************************************\n')
    f1.write('Memory contents of 0b0 - 0b100000010 (0x0 - 0x102):\n')
    memOutputSize = 10
    f1.write('Address   Value(+0)   Value(+1)   Value(+2)   Value(+3)   Value(+4)   Value(+5)   Value(+6)   Value(+7)\n')
    for i in range(0, 259):
        if (i != 0 and i % 8 == 0):
            f1.write('\n')
        if (i % 8 == 0):
            f1.write('  0x%03x ' % i)
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f1.write(' ')
        f1.write(str(memory[i]) + '| ')
    f1.write('\n****************************************************\n')
    f1.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 512
    instr_memory = []



    if (instr_logging == True):
        f = f2
    mCode = h2.readlines() 
    initializeInstrMemory(instr_memory, mCode)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] < instrCount):
        mcLine = instr_memory[registers['pc']]
        executeLine(mcLine)
        dynamInstrCount += 1
    #Output for B = 19
    f2.write('\nECE 366 Project 3\n')
    f2.write('Created by: Zhongy Chen and Claire Chappee\n')
    f2.write('Final Output for mc2.txt\n')
    f2.write('****************************************************\n')
    f2.write('Registers and their values\n')
    for key in registers:
        f2.write(register_names[key] + ' --> ' + str(registers[key]) + '\n')
    f2.write('****************************************************\n')
    f2.write('Memory contents of 0b0 - 0b100000010 (0x0 - 0x102):\n')
    memOutputSize = 10
    f2.write('Address   Value(+0)   Value(+1)   Value(+2)   Value(+3)   Value(+4)   Value(+5)   Value(+6)   Value(+7)\n')
    for i in range(0, 259):
        if (i != 0 and i % 8 == 0):
            f2.write('\n')
        if (i % 8 == 0):
            f2.write('  0x%03x ' % i)
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f2.write(' ')
        f2.write(str(memory[i]) + '| ')
    f2.write('\n****************************************************\n')
    f2.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 512
    instr_memory = []



    if (instr_logging == True):
        f = f3
    mCode = h3.readlines() 
    initializeInstrMemory(instr_memory, mCode)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] < instrCount):
        mcLine = instr_memory[registers['pc']]
        executeLine(mcLine)
        dynamInstrCount += 1
    #Output for B = E3
    f3.write('\nECE 366 Project 3\n')
    f3.write('Created by: Zhongy Chen and Claire Chappee\n')
    f3.write('Final Output for mc3.txt\n')
    f3.write('****************************************************\n')
    f3.write('Registers and their values\n')
    for key in registers:
        f3.write(register_names[key] + ' --> ' + str(registers[key]) + '\n')
    f3.write('****************************************************\n')
    f3.write('Memory contents of 0b0 - 0b100000010 (0x0 - 0x102):\n')
    memOutputSize = 10
    f3.write('Address   Value(+0)   Value(+1)   Value(+2)   Value(+3)   Value(+4)   Value(+5)   Value(+6)   Value(+7)\n')
    for i in range(0, 259):
        if (i != 0 and i % 8 == 0):
            f3.write('\n')
        if (i % 8 == 0):
            f3.write('  0x%03x ' % i)
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f3.write(' ')
        f3.write(str(memory[i]) + '| ')
    f3.write('\n****************************************************\n')
    f3.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 512
    instr_memory = []



    if (instr_logging == True):
        f = f4
    mCode = h4.readlines() 
    initializeInstrMemory(instr_memory, mCode)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] < instrCount):
        mcLine = instr_memory[registers['pc']]
        executeLine(mcLine)
        dynamInstrCount += 1
    #Output for B = 66
    f4.write('\nECE 366 Project 3\n')
    f4.write('Created by: Zhongy Chen and Claire Chappee\n')
    f4.write('Final Output for mc4.txt\n')
    f4.write('****************************************************\n')
    f4.write('Registers and their value\n')
    for key in registers:
        f4.write(register_names[key] + ' --> ' + str(registers[key]) + '\n')
    f4.write('****************************************************\n')
    f4.write('Memory contents of 0b0 - 0b100000010 (0x0 - 0x102):\n')
    memOutputSize = 10
    f4.write('Address   Value(+0)   Value(+1)   Value(+2)   Value(+3)   Value(+4)   Value(+5)   Value(+6)   Value(+7)\n')
    for i in range(0, 259):
        if (i != 0 and i % 8 == 0):
            f4.write('\n')
        if (i % 8 == 0):
            f4.write('  0x%03x ' % i)
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f4.write(' ')
        f4.write(str(memory[i]) + '| ')
    f4.write('\n****************************************************\n')
    f4.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 512
    instr_memory = []

if __name__ == "__main__":
    main()
