
# ECE 366 Project 3 Fall 2019
# Group 12: Zhongy Chen & Claire Chappee
f = 0

registers = {
        '$0': 0,
        '$1': 0,
        '$2': 0,
        '$3': 0
    }


if(line[0:2] == "00"): #lui
    rx = int(line[2:4], 2)
    imm = int(line[4:8], 4)
    imm = imm << 4
    registers[rx] = imm
    pc += 4
    dynamInstrCount += 1
    print("Instruction: lui " + str(rx) + "," + str(imm))
    print("pc is now: " + str(pc))

if(line[0:2] == "01"): #addi
    rx = int(line[2:4], 2)
    imm = int(line[4:8], 4)
    registers[Rx] = registers[Rx] + imm
    pc += 4
    dynamInstrCount += 1
    print("Instruction: addi " + str(rx) + "," + str(imm))
    print("pc is now: " + str(pc))

if(line[0:2] == "10"): #hash TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0000
    rx = int(line[2:4], 2)
    ry = int(line[4:6], 2)
    rz = int(line[6:8], 2)
    #registers[rx] = H(Ry, Rz)
    pc += 4
    dynamInstrCount += 1
    print("Instruction: hash " + str(rx) + "," + str(ry) + "," + str(rz))
    print("pc is now: " + str(pc))

if(line[0:4] == "1100"): #ldinc TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0000
    rx = int(line[4:6], 2)
    ry = int(line[6:8], 2)
    #registers[rx] = Mem[Ry] + 1
    pc += 4
    dynamInstrCount += 1
    print("Instruction: ldinc " + str(rx) + "," + "(" + str(ry) + ")" )
    print("pc is now: " + str(pc))

if(line[0:4] == "1110"): #st TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0000
    rx = int(line[4:6], 2)
    ry = int(line[6:8], 2)
    #Mem[Ry] = Rx
    pc += 4
    dynamInstrCount += 1
    print("Instruction: st " + str(rx) + "," + "(" + str(ry) + ")" )
    print("pc is now: " + str(pc))

if(line[0:4] == "1111"): #sto3inc TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0000
    rx = int(line[4:6], 2)
    ry = int(line[6:8], 2)
    #Mem[Ry + 3] = Rx 
    #Ry++
    pc += 4
    dynamInstrCount += 1
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
    func = {
        'lui': lui,
        'addi': addi,
        'hash': hash
    }
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
    global labelDict
    global instr_memory

    f1 = open("output1.txt","w+")
    h1 = open("mc1.txt","r")

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
    f1.write('Output for testcase.asm\n')
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
    labels_dict = {}
    instr_memory = []



if __name__ == "__main__":
    main()
