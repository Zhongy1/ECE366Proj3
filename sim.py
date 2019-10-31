
# ECE 366 Project 3 Fall 2019
# Group 12: Zhongy Chen & Claire Chappee

instr_logging = True
f = 0

registers = {
        '$0': 0,
        '$8': 0,
        '$9': 0,
        '$10': 0,
        '$11': 0,
        '$12': 0,
        '$13': 0,
        '$14': 0,
        '$15': 0,
        '$16': 0,
        '$17': 0,
        '$18': 0,
        '$19': 0,
        '$20': 0,
        '$21': 0,
        '$22': 0,
        '$23': 0,
        'pc': 0,
        'hi': 0,
        'lo': 0
    }

#Each element in array represents a 4 byte chunk (32 bits)
#Starts at memory location 0x2000 and ends at 0x3000
memory = [0] * 1024

#Each entry refers to a tag name as well as the line it points to
#Example: labelDict['loop1'] might have the value 3, which means the label 'loop1' refers to line 3 in instr_memory
labelDict = {}

#Each element represenets each line in assembly code
#This excludes labels, tags, and empty lines
#doing len(instr_memory) will give you the static instruction count of the program
instr_memory = []

#'options' variable for (reg1, reg2, imm)

def lui(options):
    registers[options[0]] = (int(options[1], 16 if (options[1].count('x')) else 10) << 16) | (registers[options[0]] & 0xFFFF)
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')


def addi(options):
    registers[options[0]] = (registers[options[1]] + int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')


def hash(options):
    a = registers[options[1]] & 0xFFFFFFFF
    b = registers[options[2]] & 0xFFFFFFFF
    for i in range(0, 5):
        product = a * b
        hi = product & 0xFFFFFFFF
        lo = (product >> 32) & 0xFFFFFFFF
        a = hi ^ lo
    c = (a & 0xFFFF) ^ ((a >> 16) & 0xFFFF)
    registers[options[0]] = (c & 0xFF) ^ ((c >> 8) & 0xFF)
    registers['pc'] += 4
    if (instr_logging):
        f.write('*** Special Instruction ***\n')
        f.write('\t' + options[0] + ' = H(' + options[1] + ', ' + options[2] + ')\n')
        f.write('\t' + options[0] + ' = ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def ldinc(options): #NEED TO CHANGE THE DEFINITION OF THIS FUNCTION
    registers[options[0]] = (registers[options[1]] + int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def st(options): #NEED TO CHANGE THE DEFINITION OF THIS FUNCTION
    registers[options[0]] = (registers[options[1]] + int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def sto3inc(options): #NEED TO CHANGE THE DEFINITION OF THIS FUNCTION
    registers[options[0]] = (registers[options[1]] + int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')
        
    

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

    f1 = open("outputfile.txt","w+")
    h1 = open("machinecode.txt","r")

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
