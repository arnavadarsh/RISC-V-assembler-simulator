import re

registers = {'zero': '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100', 't0': '00101', 't1': '00110', 't2': '00111',
             's0': '01000', 'fp': '01000', 's1': '01001', 'a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 
             'a4': '01110', 'a5': '01111', 'a6': '10000', 'a7': '10001', 's2': '10010', 's3': '10011', 's4': '10100', 
             's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011', 
             't3': '11100', 't4': '11101', 't5': '11110', 't6': '11111'
}

zero = '00000000000000000000000000000000'
ra = '00000000000000000000000000000000'
sp = '00000000000000000000000000000000'
gp = '00000000000000000000000000000000'
tp = '00000000000000000000000000000000'
t0 = '00000000000000000000000000000000'
t1 = '00000000000000000000000000000000'
t2 = '00000000000000000000000000000000'
s0 = fp = '00000000000000000000000000000000'
s1 = '00000000000000000000000000000000'
a0 = '00000000000000000000000000000000'
a1 = '00000000000000000000000000000000'
a2, a3, a4, a5, a6, a7 = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
s2 = '00000000000000000000000000000000'
s3 = '00000000000000000000000000000000'
s4 = '00000000000000000000000000000000'
s5 = '00000000000000000000000000000000'
s6 = '00000000000000000000000000000000'
s7 = '00000000000000000000000000000000'
s8 = '00000000000000000000000000000000'
s9 = '00000000000000000000000000000000'
s10 = '00000000000000000000000000000000'
s11 = '00000000000000000000000000000000'
t3, t4, t5, t6 = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
pc = 0




#memory
memory = {}

labels = {}

output = open('output.txt', 'w+')

def binarytodecimal(num, type='unsigned'):
    if type == 'signed':
        if num[0] == '1':
            s = 0
            s = s + (-2)**(len(num)-1)
            for i in range(1, len(num)):
                s = s + int(num[i])*(2**(len(num)-i-1))
            return s
        if num[0] == '0':
            s = 0
            for i in range(1, len(num)):
                s = s + int(num[i])*(2**(len(num)-i-1))
            return s
    else:
        s = 0
        for i in range(0, len(num)):
            s = s + int(num[i])*(2**(len(num)-i-1))
            return s
        
def signextend(digit, num, size=32):
    if len(bin(num)[2:]) > size:
        raise OverflowError('Error: Illegal immediate overflow')
    return digit*(size-len(bin(num)[2:])) + bin(num)[2:]

def decimaltobinary(num, type='unsigned', size=32):
    if type == 'signed':
        if num < 0:
            number = '0' + bin(abs(num))[2:]
            new = ''
            for i in number:
                if i == '0':
                    new = new + '1'
                else:
                    new = new + '0'
            onescomplement = int(new, 2)
            twoscomplement = onescomplement + 1
            return signextend('1', twoscomplement, size)
        if num >= 0:
            twoscomplement = num
            return signextend('0', twoscomplement, size)
    if type == 'unsigned':
        nums = num
        return signextend('0', nums, size)
    
def contains_integers(input_string):
    pattern = r'^[+-]?\d+$'
    return bool(re.match(pattern, input_string))

class assembler:
    def remove_special_characters(self, lines):
        self.new_lines = []
        for i in lines:
            j = re.sub(r'\n', '', i)
            k = re.sub(r'//.*', '', j)
            l = re.sub(r'\w+:', '', k)
            self.new_lines.append(l.strip())       
            if re.match(r'\b\w+:', k):
                labels[re.search(r'\b\w+:', k).group()] = lines.index(i)
        self.new_line = list(filter(lambda x: x != '', self.new_lines))
        return self.new_line
                
    def display(self):
        print(self.new_line)
        print(labels)
    
    def execution(self, line):
        if line == 'beq zero,zero,0':
            globals()['prev'] = globals()['pc']
            imm = decimaltobinary(0, 'signed', 12)
            output.write(imm[0]+imm[2:8]+registers['zero']+registers['zero']+'000'+imm[8:]+imm[1]+'1100011\n')
            return
        elif line.split()[0] == 'jal':
            self.jal(line)
        elif line.split()[0] == 'addi':
            self.addi(line)
        elif line.split()[0] == 'add':
            self.add(line)
        elif line.split()[0] =='sub':
            self.sub(line)
        elif line.split()[0] == 'slt':
            self.slt(line)
        elif line.split()[0] == 'sltu':
            self.sltu(line)
        elif line.split()[0] == 'sll':
            self.sll(line)
        elif line.split()[0] == 'srl':
            self.srl(line)
        elif line.split()[0] == 'or':
            self.OR(line)
        elif line.split()[0] == 'and':
            self.AND(line)
        elif line.split()[0] == 'xor':
            self.xor(line)
        elif line.split()[0] == 'lw':
            self.lw(line)
        elif line.split()[0] == 'sltiu':
            self.sltiu(line)
        elif line.split()[0] == 'jalr':
            self.jalr(line)
        elif line.split()[0] == 'sw':
            self.sw(line)
        elif line.split()[0] == 'beq':
            self.beq(line)
        elif line.split()[0] == 'bne':
            self.bne(line)
        elif line.split()[0] == 'bge':
            self.bge(line)
        elif line.split()[0] == 'bgeu':
            self.bgeu(line)
        elif line.split()[0] == 'blt':
            self.blt(line)
        elif line.split()[0] == 'bltu':
            self.bltu(line)
        elif line.split()[0] == 'auipc':
            self.auipc(line)
        elif line.split()[0] == 'lui':
            self.lui(line)
        elif line.split()[0] == 'jal':
            self.jal(line)
        else:
            print('Error: Invalid instruction')
            return
            
    def addi(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            try:
                imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') + int(line.split()[1].split(',')[2]), 'signed', 32)
                globals()['pc'] = globals()['pc'] + 4
                output.write(decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)+registers[line.split()[1].split(',')[1]]+'000'+registers[line.split()[1].split(',')[0]]+'0010011\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return
            
        
    def add(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') + binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'000'+registers[line.split()[1].split(',')[0]]+'0110011\n')
    
    def sub(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') - binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0100000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'000'+registers[line.split()[1].split(',')[0]]+'0110011\n')
        
    def sll(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') << binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'001'+registers[line.split()[1].split(',')[0]]+'0110011\n')
    
    def srl(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') >> binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'101'+registers[line.split()[1].split(',')[0]]+'0110011\n')
            
    def slt(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            if binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') < binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'):
                globals()[line.split()[1].split(',')[0]] = decimaltobinary(1, 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'010'+registers[line.split()[1].split(',')[0]]+'0110011\n')
    
    def sltu(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            if binarytodecimal(globals()[line.split()[1].split(',')[1]], 'unsigned') < binarytodecimal(globals()[line.split()[1].split(',')[2]], 'unsigned'):
                globals()[line.split()[1].split(',')[0]] = decimaltobinary(1, 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'011'+registers[line.split()[1].split(',')[0]]+'0110011\n')
    
    def OR(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed')|binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'110'+registers[line.split()[1].split(',')[0]]+'0110011\n')
    
    def AND(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') & binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'111'+registers[line.split()[1].split(',')[0]]+'0110011\n')
    
    def xor(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals() or line.split()[1].split(',')[2] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals() and line.split()[1].split(',')[2] in globals():
            globals()[line.split()[1].split(',')[0]] = decimaltobinary(binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed') ^ binarytodecimal(globals()[line.split()[1].split(',')[2]], 'signed'), 'signed')
            globals()['pc'] = globals()['pc'] + 4
            output.write('0000000'+registers[line.split()[1].split(',')[2]]+registers[line.split()[1].split(',')[1]]+'100'+registers[line.split()[1].split(',')[0]]+'0110011\n')
            
    def lw(self, line):
        globals()['prev'] = globals()['pc']
        src_reg = re.findall(r'\b\w+\s*,\s*(-?\d+)\((\w+)\)', line)[0][1]
        imm = re.findall(r'\b\w+\s*,\s*(-?\d+)\((\w+)\)', line)[0][0]
        if line.split()[1].split(',')[0] not in globals() or src_reg not in globals():
            print('Error: No such register')
            return
        if not contains_integers(imm):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and src_reg in globals():
            stored = binarytodecimal(globals()[src_reg], 'signed')
            try:
                immediate = decimaltobinary(int(imm), 'signed', 12)
                if str(int(imm) + stored) not in memory:
                    globals()[line.split()[1].split(',')[0]] = '00000000000000000000000000000000'
                else:
                    globals()[line.split()[1].split(',')[0]] = memory[str(int(imm) + stored)]
                globals()['pc'] = globals()['pc'] + 4
                output.write(immediate+registers[src_reg]+'010'+registers[line.split()[1].split(',')[0]]+'0000011\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return

    def sltiu(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            imm = int(line.split()[1].split(',')[2])
            try:
                immediate = decimaltobinary(imm, 'unsigned', 12)
                rs = binarytodecimal(globals()[line.split()[1].split(',')[1]])
                if rs < imm:
                    globals()[line.split()[1].split(',')[0]] = decimaltobinary(1, 'signed')
                globals()['pc'] = globals()['pc'] + 4
                output.write(immediate+registers[line.split()[1].split(',')[1]]+'011'+registers[line.split()[1].split(',')[0]]+'0010011\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return
                
    def jalr(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            imm = int(line.split()[1].split(',')[2])
            try:
                immediate = decimaltobinary(imm, 'signed', 12)    
                stored = binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed')
                globals()[line.split()[1].split(',')[0]] = decimaltobinary(globals()['pc'] + 4, 'signed')
                globals()['pc'] = (stored + imm) & ~1
                output.write(immediate+registers[line.split()[1].split(',')[1]]+'000'+registers[line.split()[1].split(',')[0]]+'1100111\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return
    
    def sw(self, line):
        globals()['prev'] = globals()['pc']
        src_reg = re.findall(r'\b\w+\s*,\s*(-?\d+)\((\w+)\)', line)[0][1]
        imm = re.findall(r'\b\w+\s*,\s*(-?\d+)\((\w+)\)', line)[0][0]
        if src_reg not in globals() or line.split()[1].split(',')[0] not in globals():
            print('Error: No such register')
            return
        if not contains_integers(imm):
            print('Error: Invalid immediate')
            return            
        if line.split()[1].split(',')[0] in globals() and src_reg in globals():
            stored = binarytodecimal(globals()[src_reg], 'signed')
            try:
                immediate = decimaltobinary(int(imm), 'signed', 12)
                memory[str(int(imm) + stored)] = globals()[line.split()[1].split(',')[0]]
                globals()['pc'] = globals()['pc'] + 4
                output.write(immediate[:7]+registers[line.split()[1].split(',')[0]]+registers[src_reg]+'010'+immediate[7:]+'0100011\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return
    
    def beq(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[2]+':' not in globals()['labels'] and not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            if line.split()[1].split(',')[2]+':' not in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]]) == binarytodecimal(globals()[line.split()[1].split(',')[1]]):
                    try:
                        imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                        globals()['pc'] = globals()['pc'] + int(line.split()[1].split(',')[2]) + 4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
            elif line.split()[1].split(',')[2]+':' in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]], 'signed') == binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed'):
                    try:
                        imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                        globals()['pc'] = labels[line.split()[1].split(',')[2]+':']*4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4),'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
                
    def bne(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if line.split(',')[1].split(',')[2]+':' not in globals()['labels'] and not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():             #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if line.split()[1].split(',')[2]+':' not in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]]) != binarytodecimal(globals()[line.split()[1].split(',')[1]]):
                    try:
                        imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                        globals()['pc'] = globals()['pc'] + int(line.split()[1].split(',')[2]) + 4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
            elif line.split()[1].split(',')[2]+':' in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]], 'signed') != binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed'):
                    try:
                        imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                        globals()['pc'] = labels[line.split()[1].split(',')[2]+':']*4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'000'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
    
    def bge(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() and line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[2]+':' not in globals()['labels'] and not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            if line.split()[1].split(',')[2]+':' not in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]], 'signed') >= binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed'):
                    try:
                        imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                        globals()['pc'] = globals()['pc'] + int(line.split()[1].split(',')[2]) + 4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'101'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'101'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
            elif line.split()[1].split(',')[2]+':' in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]], 'signed') >= binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed'):
                    try:
                        imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']-(globals()['pc']+4),'signed', 12)
                        globals()['pc'] = labels[line.split()[1].split(',')[2]+':']*4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'101'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'101'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
                
    def bgeu(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[2]+':' not in globals()['labels'] and not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return 
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            if line.split()[1].split(',')[2]+':' not in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]]) >= binarytodecimal(globals()[line.split()[1].split(',')[1]]):
                    try:
                        imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                        globals()['pc'] = globals()['pc'] + int(line.split()[1].split(',')[2]) + 4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'111'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'111'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
            elif line.split()[1].split(',')[2]+':' in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]]) >= binarytodecimal(globals()[line.split()[1].split(',')[1]]):
                    try:
                        imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                        globals()['pc'] = labels[line.split()[1].split(',')[2]+':']*4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'111'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'111'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return                
                
    def blt(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register')
            return
        if line.split()[1].split(',')[2]+':' not in globals()['labels'] and not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            if line.split()[1].split(',')[2]+':' not in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]], 'signed') < binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed'):
                    try:
                        imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                        globals()['pc'] = globals()['pc'] + int(line.split()[1].split(',')[2]) + 4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'100'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'100'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
            elif line.split()[1].split(',')[2]+':' in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]], 'signed') < binarytodecimal(globals()[line.split()[1].split(',')[1]], 'signed'):
                    try:
                        imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4), 'signed', 12)
                        globals()['pc'] = labels[line.split()[1].split(',')[2]+':']*4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'100'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4),'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'100'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
    
    def bltu(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals() or line.split()[1].split(',')[1] not in globals():
            print('Error: No such register or invalid immediate')
            return
        if line.split()[1].split(',')[2]+':' not in globals()['labels'] and not contains_integers(line.split()[1].split(',')[2]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals() and line.split()[1].split(',')[1] in globals():
            if line.split()[1].split(',')[2]+':' not in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]]) < binarytodecimal(globals()[line.split()[1].split(',')[1]]):
                    try:
                        imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                        globals()['pc'] = int(line.split()[1].split(',')[2]) + 4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'110'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(int(line.split()[1].split(',')[2]), 'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'110'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
            elif line.split()[1].split(',')[2]+':' in globals()['labels']:
                if binarytodecimal(globals()[line.split()[1].split(',')[0]]) < binarytodecimal(globals()[line.split()[1].split(',')[1]]):
                    try:
                        imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()[pc]+4),'signed', 12)
                        globals()['pc'] = labels[line.split()[1].split(',')[2]+':']*4
                        output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'110'+imm[8:]+imm[1]+'1100011\n')
                        return
                    except OverflowError:
                        print('Error: Illegal immediate length')
                        return
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[2]+':']*4-(globals()['pc']+4),'signed', 12)
                    globals()['pc'] = globals()['pc'] + 4
                    output.write(imm[0]+imm[2:8]+registers[line.split()[1].split(',')[1]]+registers[line.split()[1].split(',')[0]]+'110'+imm[8:]+imm[1]+'1100011\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
                
    def auipc(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals():
            print('Error: No such register')
            return
        if not contains_integers(line.split()[1].split(',')[1]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals():
            imm = int(line.split()[1].split(',')[1])
            imm1 = imm << 12
            try:
                immediate = decimaltobinary(imm, 'signed', 20)
                globals()[line.split()[1].split(',')[0]] = decimaltobinary(globals()['pc'] + imm1, 'signed')
                globals()['pc'] = globals()['pc'] + 4
                output.write(decimaltobinary(imm, 'signed', 20)+registers[line.split()[1].split(',')[0]]+'0010111\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return
    
    def lui(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals():
            print('Error: No such register')
            return
        if not contains_integers(line.split()[1].split(',')[1]):
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals():
            imm = int(line.split()[1].split(',')[1])
            imm1 = imm << 12
            try:
                immediate = decimaltobinary(imm, 'signed', 20)
                globals()[line.split()[1].split(',')[0]] = decimaltobinary(imm1, 'signed')
                globals()['pc'] = globals()['pc'] + 4
                output.write(decimaltobinary(imm, 'signed', 20)+registers[line.split()[1].split(',')[0]]+'0010111\n')
            except OverflowError:
                print('Error: Illegal immediate length')
                return
    
    def jal(self, line):
        globals()['prev'] = globals()['pc']
        if line.split()[1].split(',')[0] not in globals():
            print('Error: No such register')
            return
        if not contains_integers(line.split()[1].split(',')[1]) and line.split()[1].split(',')[1]+':' not in globals()['labels']:
            print('Error: Invalid immediate')
            return
        if line.split()[1].split(',')[0] in globals():
            if line.split()[1].split(',')[1]+':' not in globals()['labels']:
                imm = int(line.split()[1].split(',')[1])
                try:
                    imm1 = decimaltobinary(imm, 'signed', 20)
                    globals()[line.split()[1].split(',')[0]] = decimaltobinary(globals()['pc'] + 4, 'signed')
                    globals()['pc'] = globals()['pc'] + imm + 4
                    output.write(imm1[0]+imm1[10:]+imm1[9]+imm1[1:9]+registers[line.split()[1].split(',')[0]]+'0010111\n')
                except OverflowError:
                    globals()['prev'] = globals()['pc']
                    print('Error: illegal immediate length')
                    return
            elif line.split()[1].split(',')[1]+':' in globals()['labels']:
                try:
                    imm = decimaltobinary(labels[line.split()[1].split(',')[1]+':']*4-(globals()['pc']+4), 'signed', 20)
                    globals()[line.split()[1].split(',')[0]] = decimaltobinary(globals()['pc'] + 4, 'signed')
                    globals()['pc'] = labels[line.split()[1].split(',')[1]+':']*4
                    output.write(imm[0]+imm[10:]+imm[1:9]+registers[line.split()[1].split(',')[0]]+'0010111\n')
                except OverflowError:
                    print('Error: Illegal immediate length')
                    return
                    
with open('text.txt', 'r') as f:
    lines = f.readlines()

x = assembler()
new_lines = x.remove_special_characters(lines)

prev = None

if 'beq zero,zero,0' not in new_lines:
    print('Error: Missing virtual halt')
    prev = pc
    
for label in labels:
    if label.replace(' ', '') != label:
        print('Error: Invalid labels')
        prev = pc

while prev != pc:
    x.execution(new_lines[int(pc//4)])
    print(pc)
    
output.close()
