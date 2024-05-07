registers = {'00000': 'zero', '00001': 'ra', '00010': 'sp', '00011': 'gp', '00100': 'tp', '00101': 't0', '00110': 't1', '00111': 't2',
             '01000': 's0', '01001': 's1', '01010': 'a0', '01011': 'a1', '01100': 'a2', '01101': 'a3',
             '01110': 'a4', '01111': 'a5', '10000': 'a6', '10001': 'a7', '10010': 's2', '10011': 's3', '10100': 's4',
             '10101': 's5', '10110': 's6', '10111': 's7', '11000': 's8', '11001': 's9', '11010': 's10', '11011': 's11',
             '11100': 't3', '11101': 't4', '11110': 't5', '11111': 't6'
}

output = open('output.txt', 'w+')

zero = ra = sp = gp = tp = t0 = t1 = t2 = s0 = s1 = a0 = a1 = '00000000000000000000000000000000'
a2 = a3 = a4 = a5 = a6 = a7 = s2 = s3 = s4 = s5 = s6 = s7 = '00000000000000000000000000000000'
s8 = s9 = s10 = s11 = t3 = t4 = t5 = t6 = '00000000000000000000000000000000'
pc = 4

memory = {i: '00000000000000000000000000000000' for i in range(65536, 65661, 4)}
def binarytodecimal(num, type='unsigned'):
    s = 0
    i = 0
    if type == 'signed':
        if num[0] == '1':
            s -= 2**(len(num)-1)
            i = 1
        while i < len(num):
            s += int(num[i]) * (2**(len(num)-i-1))
            i += 1
    else:
        while i < len(num):
            s += int(num[i]) * (2**(len(num)-i-1))
            i += 1
    return s

def signextend(digit, num, size=32):
    if len(bin(num)[2:]) > size:
        raise OverflowError('Error: Illegal immediate overflow')
    return digit*(size-len(bin(num)[2:])) + bin(num)[2:]

def decimaltobinary(num, type='unsigned', size=32):
    global output
    if type == 'signed':
        if num < 0:
            number = '0' + bin(abs(num))[2:]
            new = ''.join('1' if i == '0' else '0' for i in number)
            onescomplement = int(new, 2)
            twoscomplement = onescomplement + 1
            return signextend('1', twoscomplement, size)
        else:
            return signextend('0', num, size)
    else:
        if num < 0:
            raise OverflowError('Error: Illegal immediate overflow')
        return signextend('0', num, size)
class simulator:
    def execution(self, line):
        if line[-7:] == '0110011' and line[:7] == '0100000' and line[17:20] == '000':
            self.sub(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '000':
            self.add(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '001':
            self.sll(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '010':
            self.slt(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '011':
            self.sltu(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '100':
            self.xor(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '101':
            self.srl(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '110':
            self.OR(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '111':
            self.AND(line)
            return
        elif line[-7:] == '0000011' and line[17:20] == '010':
            self.lw(line)
            return
        elif line[-7:] == '0010011' and line[17:20] == '000':
            self.addi(line)
            return
        elif line[-7:] == '0010011' and line[17:20] == '011':
            self.sltiu(line)
            return
        elif line[-7:] == '1100111' and line[17:20] == '000':
            self.jalr(line)
            return
        elif line[-7:] == '0100011' and line[17:20] == '010':
            self.sw(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '000':
            self.beq(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '001':
            self.bne(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '100':
            self.blt(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '101':
            self.bge(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '110':
            self.bgeu(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '111':
            self.bltu(line)
            return
        elif line[-7:] == '0110111':
            self.lui(line)
            return
        elif line[-7:] == '0010111':
            self.auipc(line)
            return
        elif line[-7:] == '1101111':
            self.jal(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '000':
            self.mul(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '001':
            self.rst(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '010':
            self.halt(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '011':
            self.rvrs(line)
            return
    
    def add(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sub(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') - binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sll(self, line):
        
        imm = binarytodecimal(globals()[registers[line[7:12]]][-5:])
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') << binarytodecimal(imm), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4

    def slt(self, line):
        
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') < binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
            
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sltu(self, line):
        
        if binarytodecimal(globals()[registers[line[12:17]]]) < binarytodecimal(globals()[registers[line[7:12]]]):
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def xor(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') ^ binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def srl(self, line):
        
        imm = binarytodecimal(globals()[registers[line[7:12]]][-5:])
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') >> imm, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def OR(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') | binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def AND(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') & binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def lw(self, line):
        
        globals()[registers[line[20:25]]] = memory[binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:12], 'signed')]
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def addi(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:12], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sltiu(self, line):
        
        if binarytodecimal(globals()[registers[line[12:17]]]) < binarytodecimal(line[:12]):
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def jalr(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + 4, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['pc'] = (binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:12], 'signed')) & ~1
        output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
                
    def sw(self, line):
        
        
        memory[binarytodecimal(globals()[registers[line[12:17]]], 'signed')+binarytodecimal(line[:7]+line[20:25], 'signed')] = globals()[registers[line[7:12]]]
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4 
    
    def beq(self, line):
        
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') == binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
    
    def bne(self, line):
        globals()['zero'] = '00000000000000000000000000000000'
        
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') != binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
            
    
    def blt(self, line):
        
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') < binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4

    def bge(self, line):
        
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') > binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
    
    def bltu(self, line):
        
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]]) < binarytodecimal(globals()[registers[line[7:12]]]):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
    
    def bgeu(self, line):
        
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]]) > binarytodecimal(globals()[registers[line[7:12]]]):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
            
    def auipc(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + binarytodecimal(line[:20]+'000000000000', 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
        
    def lui(self, line):
        
        globals()[registers[line[20:25]]] = line[:20]+'000000000000'
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def jal(self, line):
        
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + 4, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['pc'] += (binarytodecimal(line[0]+line[12:20]+line[11]+line[1:11]+'0', 'signed')) & ~1
        output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        
    def mul(self, line):
        globals()['pc'] += 4
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') * binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
                
    def rst(self, line):
        globals()['pc'] += 4
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['ra'] = '00000000000000000000000000000000'
        globals()['sp'] = '00000000000000000000000000000000'
        globals()['gp'] = '00000000000000000000000000000000'
        globals()['tp'] = '00000000000000000000000000000000'
        globals()['t0'] = '00000000000000000000000000000000'
        globals()['t1'] = '00000000000000000000000000000000'
        globals()['t2'] = '00000000000000000000000000000000'
        globals()['s0'] = '00000000000000000000000000000000'
        globals()['s1'] = '00000000000000000000000000000000'
        globals()['a0'] = '00000000000000000000000000000000'
        globals()['a1'] = '00000000000000000000000000000000'
        globals()['a2'], globals()['a3'], globals()['a4'], globals()['a5'], globals()['a6'], globals()['a7'] = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
        globals()['s2'] = '00000000000000000000000000000000'
        globals()['s3'] = '00000000000000000000000000000000'
        globals()['s4'] = '00000000000000000000000000000000'
        globals()['s5'] = '00000000000000000000000000000000'
        globals()['s6'] = '00000000000000000000000000000000'
        globals()['s7'] = '00000000000000000000000000000000'
        globals()['s8'] = '00000000000000000000000000000000'
        globals()['s9'] = '00000000000000000000000000000000'
        globals()['s10'] = '00000000000000000000000000000000'
        globals()['s11'] = '00000000000000000000000000000000'
        globals()['t3'], globals()['t4'], globals()['t5'], globals()['t6'] = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            
    def rvrs(self, line):
        globals()['pc'] += 4
        globals()[registers[line[20:25]]] = globals()[registers[line[12:17]]][::-1]
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        
        
        
        
input_file = open('text.txt', 'r')

l = input_file.readlines()

l = [i.strip('\n') for i in l]

x = simulator()

while int(pc//4)-1 < len(l):
    if l[int(pc//4)-1] == '00000000000000000000000001100011':
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        break
    if l[int(pc//4)-1] == '00000000000000000010000001110001':
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        break
    x.execution(l[int(pc//4)-1])
    
for i in memory:
    output.write('0x000'+hex(i)[2:]+':'+'0b'+memory[i]+'\n')


output.close()