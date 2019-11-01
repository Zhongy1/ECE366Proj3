# ECE 366 Project 3 Fall 2019
# Group 12: Zhongy Chen & Claire Chappee
f = 0
instr_logging = True

registers = {
        '00': 0,
        '01': 0,
        '10': 0,
        '11': 0,
        'pc': 0
    }

#2^9 needs to be the size of our memory
memory = [0] * 512

def myFunc(line):
    if(line[0:2] == "00"): #lui
        rx = int(line[2:4], 2)
        imm = int(line[4:8], 4)
        imm = imm << 4
        registers[rx] = imm
        pc += 1
        print("Instruction: lui " + str(rx) + "," + str(imm))
        print("pc is now: " + str(pc))

    if(line[0:2] == "01"): #addi
        rx = int(line[2:4], 2)
        imm = int(line[4:8], 4)
        registers[rx] = registers[rx] + imm
        pc += 1
        print("Instruction: addi " + str(rx) + "," + str(imm))
        print("pc is now: " + str(pc))

    if(line[0:2] == "10"): #hash 
        rx = int(line[2:4], 2)
        ry = int(line[4:6], 2)
        rz = int(line[6:8], 2)
        #registers[rx] = H(ry, rz)
        for i in range(0, 5):
            srcA = ry
            srcB = rz
            temp = srcA * srcB
            hi = (temp ^ 0xFF00) >> 8
            lo = temp ^ 0xFF
            srcA = hi ^ lo
        pc += 1
        print("Instruction: hash " + str(rx) + "," + str(ry) + "," + str(rz))
        print("pc is now: " + str(pc))

    if(line[0:4] == "1100"): #ldinc
        rx = int(line[4:6], 2)
        ry = int(line[6:8], 2)
        registers[rx] = memory[int(ry,2)] + 1
        pc += 1
        print("Instruction: ldinc " + str(rx) + "," + "(" + str(ry) + ")" )
        print("pc is now: " + str(pc))

    if(line[0:4] == "1110"): #st 
        rx = int(line[4:6], 2)
        ry = int(line[6:8], 2)
        memory[int(ry,2)] = registers[rx]
        pc += 1
        print("Instruction: st " + str(rx) + "," + "(" + str(ry) + ")" )
        print("pc is now: " + str(pc))

    if(line[0:4] == "1111"): #sto3inc 
        rx = int(line[4:6], 2)
        ry = int(line[6:8], 2)
        valRX = registers[rx]
        srcA = registers[ry]
        srcB = 3
        aluResult = srcA + srcB
        memory[aluResult] = valRX
        registers[ry] += 1
        pc += 1
        print("Instruction: sto3inc " + str(rx) + "," + "(" + str(ry) + ")" )
        print("pc is now: " + str(pc))

def initializeInstrMemory(instr_mem_array, labels_dict, asm):
    index = 0
    for line in asm:
        line = line.strip()
        if (line == ''):
            continue
        if (line.count(":")):
            labels_dict[line[0:line.index(":")]] = index
        else:
            index += 1
            instr_mem_array.append(line)

class Instruction:
    def __init__(self, instrStr):
        self.str = instrStr
        instrParts = instrStr.split(' ', 1)
        self.f_type = instrParts[0]
        instrParts = instrParts[1].split(',')
        for i in range(0,len(instrParts)):
            if (instrParts[i].count('(')):
                spec = instrParts[i]
                instrParts.pop()
                instrParts.append(spec[0:spec.index('(')].strip())
                instrParts.append(spec[spec.index('(')+1:spec.index(')')].strip())
                break
            instrParts[i] = instrParts[i].strip()
        self.instrVals = instrParts
    
    def execute(self):
        self.func[self.f_type](self.instrVals)

    def toString(self):
        return self.str

def main():
    global f
    global registers
    global memory

    f1 = open("output1.txt","w+")
    h1 = open("mc1.txt","r")
    f2 = open("output2.txt","w+")
    h2 = open("mc2.txt","r")
    f3 = open("output3.txt","w+")
    h3 = open("mc3.txt","r")
    f4 = open("output4.txt","w+")
    h4 = open("mc4.txt","r")

    if (instr_logging == True):
        f = f1
    asm = h1.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f1.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Testcase Output
    f1.write('ECE 366 Project 3\n')
    f1.write('Created by: Zhongy Chen and Claire Chappee\n')
    f1.write('Output for mc1.txt\n')
    f1.write('****************************************************\n')
    for key in registers:
        f1.write(key + ' --> ' + str(registers[key]) + '\n')
    f1.write('****************************************************\n')
    f1.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 12
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f1.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f1.write(' ')
        f1.write(str(memory[i]) + ' ')
    f1.write('\n****************************************************\n')
    f1.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 1024

    if (instr_logging == True):
        f = f2
    asm = h2.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f2.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Testcase Output
    f2.write('ECE 366 Project 3\n')
    f2.write('Created by: Zhongy Chen and Claire Chappee\n')
    f2.write('Output for mc2.txt\n')
    f2.write('****************************************************\n')
    for key in registers:
        f2.write(key + ' --> ' + str(registers[key]) + '\n')
    f2.write('****************************************************\n')
    f2.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 12
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f2.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f2.write(' ')
        f2.write(str(memory[i]) + ' ')
    f2.write('\n****************************************************\n')
    f2.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 1024

    if (instr_logging == True):
        f = f3
    asm = h3.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f3.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Testcase Output
    f3.write('ECE 366 Project 3\n')
    f3.write('Created by: Zhongy Chen and Claire Chappee\n')
    f3.write('Output for mc3.txt\n')
    f3.write('****************************************************\n')
    for key in registers:
        f3.write(key + ' --> ' + str(registers[key]) + '\n')
    f3.write('****************************************************\n')
    f3.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 12
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f3.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f3.write(' ')
        f3.write(str(memory[i]) + ' ')
    f3.write('\n****************************************************\n')
    f3.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 1024

    if (instr_logging == True):
        f = f4
    asm = h4.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f4.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Testcase Output
    f4.write('ECE 366 Project 3\n')
    f4.write('Created by: Zhongy Chen and Claire Chappee\n')
    f4.write('Output for mc4.txt\n')
    f4.write('****************************************************\n')
    for key in registers:
        f4.write(key + ' --> ' + str(registers[key]) + '\n')
    f4.write('****************************************************\n')
    f4.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 12
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f4.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f4.write(' ')
        f4.write(str(memory[i]) + ' ')
    f4.write('\n****************************************************\n')
    f4.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 512


if __name__ == "__main__":
    main()
