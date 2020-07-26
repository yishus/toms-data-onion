class Vm:
    def __init__(self, bytes):
        self.program = bytes

        # registers
        self.a = self.b = self.c = self.f = self.ptr = self.pc = 0
        self.one_a = self.one_b = self.one_c = self.one_d = 0
    
    def run(self):
        while self.program[self.pc] != 0x01:
            self.execute()

    def execute(self):
        current = self.program[self.pc]
        b = format(self.program[self.pc], '08b')
        if current == 0xc2:
            # ADD
            self.pc += 1
            self.a = (self.a + self.b) % 256
        elif current == 0xe1:
            # APTR imm8
            self.pc += 2
            self.ptr += self.program[self.pc - 1]
        elif current == 0xc1:
            # CMP
            self.pc += 1
            if self.a == self.b:
                self.f = 0
            else:
                self.f = 1
        elif current == 0x21:
            # JEZ imm32
            self.pc += 5
            if self.f == 0:
                self.pc = int.from_bytes(self.program[self.pc - 4 : self.pc], byteorder='little')
        elif current == 0x22:
            # JNZ imm32
            self.pc += 5
            if self.f != 0:
                self.pc = int.from_bytes(self.program[self.pc - 4 : self.pc], byteorder='little')
        elif current == 0x02:
            # OUT a
            self.pc += 1
            print(chr(self.a), end =" ") 
        elif current == 0xc3:
            # SUB a <- b
            self.pc += 1
            sub = self.a - self.b
            if sub < 0:
                sub += 255
            self.a = sub
        elif current == 0xc4:
            # XOR a <- b
            self.pc += 1
            self.a = self.a ^ self.b
        elif b[:2] == "01":
            if b[-3:] == "000":
                # MVI dest imm8
                self.pc += 2
                self.dest(b[2:5], self.program[self.pc - 1])
            else:
                # MV dest src
                self.pc += 1
                self.dest(b[2:5], self.dest_val(b[5:8]))
        elif b[:2] == "10":
            if b[-3:] == "000":
                # MVI dest imm32
                self.pc += 5
                self.dest_32(b[2:5], int.from_bytes(self.program[self.pc - 4 : self.pc], byteorder='little'))
            else:
                # MV32 dest src
                self.pc += 1
                self.dest_32(b[2:5], self.dest_32_val(b[5:8]))
        else:
            raise ValueError("Incorrect opcode: " + current)
            
        
    def dest(self, str, val):
        if str == "001":
            self.a = val
        elif str == "010":
            self.b = val
        elif str == "011":
            self.c = val
        elif str == "100":
            self.d = val
        elif str == "101":
            self.e = val
        elif str == "110":
            self.f = val
        elif str == "111":
            self.program[self.ptr + self.c] = val

    def dest_val(self, str):
        if str == "001":
            return self.a
        elif str == "010":
            return self.b
        elif str == "011":
            return self.c
        elif str == "100":
            return self.d
        elif str == "101":
            return self.e
        elif str == "110":
            return self.f
        elif str == "111":
            return self.program[self.ptr + self.c]

    def dest_32(self, str, val):
        if str == "001":
            self.one_a = val
        elif str == "010":
            self.one_b = val
        elif str == "011":
            self.one_c = val
        elif str == "100":
            self.one_d = val
        elif str == "101":
            self.ptr = val
        elif str == "110":
            self.pc = val


    def dest_32_val(self, str):
        if str == "001":
            return self.one_a
        elif str == "010":
            return self.one_b
        elif str == "011":
            return self.one_c
        elif str == "100":
            return self.one_d
        elif str == "101":
            return self.ptr
        elif str == "110":
            return self.pc
        
        
            

