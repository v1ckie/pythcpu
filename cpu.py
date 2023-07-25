import random
import numpy as np

"""
MEM-MAP CPU
"""

class value():

    def __init__(self, startingValue, maxValue, minValue=None):
        self.Value = startingValue
        self.Max = maxValue
        self.Min = minValue or self.Value
        self.Overflow = False
        self.Underflow = False

    def get(self):
        return self.Value
        
    def set(self, x):
        if x > self.Max:
            self.Overflow = True
            self.Value = x % self.Max
        elif x < self.Min:
            self.Underflow = True
            self.Value = x % self.Max
        else:
            self.Value = x

    # Resets
    def resetOverflow(self):
        self.Overflow = False
    def resetUnderflow(self):
        self.Underflow = False
    def reset(self):
        self.Overflow = False
        self.Underflow = False
        
    def clear(self):
        self.value = self.Min

class counter(value):
    def increment(self):
        self.set(self.get() + 1)
    def decrement(self):
        self.set(self.get() - 1)

class stack():

    def __init__(self):
        self.stack = []
        self.count = counter(0, 255)
        
    def empty(self):
        self.stack = []
        self.count.set(0)

    def push(self, v):
        self.count.increment()
        self.stack.append(v)

    def pop(self):
        temp = self.stack[self.count.get()]
        del self.stack[self.count.get()]
        self.count.decrement()
        return temp

    def peak(self):
        return self.stack[self.count.get()]

class cpu():

    def __init__(self):
        self.memory = np.zeros((2**16)-1)
        #self.memory = None
        self.A = value(0,255)
        self.B = value(0,255)
        self.X = value(0,255)
        self.Y = value(0,255)
        self.ProgramCounter = counter(0, (2**16)-1)
        self.Instruction = 0
        self.status = [
            False, #Running
            False, #Equal
            False, #More
            False, #Less
            False, #Interrupts enabled?
            False, #In an interrupt?
        ]
        self.stack = stack()
        self.returnStack = stack()

    def updateMem(self):
        self.memory[0] = self.A.get()
        self.memory[1] = self.B.get()
        self.memory[2] = self.X.get()
        self.memory[3] = self.Y.get()
    
    def tick(self):
        # Fetch
        self.Instruction = self.memory[self.ProgramCounter.get()]
        # Decode and Execute
        match self.Instruction:
            case 0:
                #No op
                pass
            case 1:
                # Zero A
                self.A.set(0)
            case 2:
                # zero B
                self.B.set(0)
            case 3:
                # Zero X
                self.X.set(0)
            case 4:
                # Zero Y
                self.Y.set(0)
            case 5:
                # Swap A and B
                temp = self.A.get()
                self.A.set(self.B.get())
                self.B.set(temp)
                del temp
            case 6:
                # Swap X and Y
                temp = self.X.get()
                self.X.set(self.Y.get())
                self.Y.set(temp)
                del temp
            case 7:
                # Swap A and X
                temp = self.A.get()
                self.A.set(self.X.get())
                self.X.set(temp)
                del temp
            case 8:
                # Swap B and Y
                temp = self.B.get()
                self.B.set(self.Y.get())
                self.Y.set(temp)
                del temp
            case 9:
                # inc A
                self.A.set(self.A.get() + 1)
            case 10:
                # inc B
                self.B.set(self.B.get() + 1)
            case 11:
                # inc X
                self.X.set(self.X.get() + 1)
            case 12:
                # inc Y
                self.Y.set(self.Y.get() + 1)
            case 13:
                # dec A
                self.A.set(self.A.get() - 1)
            case 14:
                # dec B
                self.B.set(self.B.get() - 1)
            case 15:
                # dec X
                self.X.set(self.X.get() - 1)
            case 16:
                # dec y
                self.Y.set(self.Y.get() - 1)
            case 17:
                # zero mem[arg]
                self.ProgramCounter.increment() 
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[arg] = 0
            case 18:
                # zero mem[a]
                self.memory[self.A.get()] = 0
            case 19:
                # zero mem[b]
                self.memory[self.B.get()] = 0
            case 20:
                # zero mem[[arg]]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[self.memory[arg]] = 0
            case 21:
                # zero mem[[a]]
                self.memory[self.memory[self.A.get()]] = 0
            case 22:
                # zero mem[[b]]
                self.memory[self.memory[self.B.get()]] = 0
            case 23:
                # inc mem[arg]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[arg] = self.memory[arg] + 1
            case 24:
                # inc mem[a]
                self.memory[self.A.get()] = self.memory[self.A.get()] + 1
            case 25:
                # inc mem[b]
                self.memory[self.B.get()] = self.memory[self.B.get()] + 1
            case 26:
                # inc mem[[arg]]
                self.ProgramCounter.incremet()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[self.memory[arg]] = self.memory[self.memory[arg]] + 1
            case 27:
                # inc mem[[a]]
                self.memory[self.memory[self.A.get()]] = self.memory[self.memory[self.A.get()]] + 1
            case 28:
                # inc mem[[b]]
                self.memory[self.memory[self.B.get()]] = self.memory[self.memory[self.B.get()]] + 1
            case 29:
                # inc mem[arg]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[arg] = self.memory[arg] - 1
            case 30:
                # dec mem[a]
                self.memory[self.A.get()] = self.memory[self.A.get()] - 1
            case 31:
                # dec mem[b]
                self.memory[self.B.get()] = self.memory[self.B.get()] - 1
            case 32:
                # dec mem[[arg]]
                self.ProgramCounter.incremet()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[self.memory[arg]] = self.memory[self.memory[arg]] - 1
            case 33:
                # dec mem[[a]]
                self.memory[self.memory[self.A.get()]] = self.memory[self.memory[self.A.get()]] - 1
            case 34:
                # dec mem[[b]]
                self.memory[self.memory[self.B.get()]] = self.memory[self.memory[self.B.get()]] - 1
            case 35:
                # lda mem[arg]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.A.set(self.memory[arg])
            case 36:
                # lda mem[[arg]]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.A.set(self.memory[self.memory[arg]])
            case 37:
                # lda mem[b]
                self.A.set(self.memory[self.B.get()])
            case 38:
                # lda arg
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.A.set(arg)
            case 39:
                # ldb mem[arg]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.B.set(self.memory[arg])
            case 40:
                # ldb mem[[arg]]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.B.set(self.memory[self.memory[arg]])
            case 41:
                # ldb mem[a]
                self.B.set(self.memory[self.B.get()])
            case 42:
                # ldb arg
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.B.set(arg)
            case 43:
                # sta mem[arg]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[arg] = self.A.get()
            case 44:
                # sta mem[[arg]]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[self.memory[arg]] = self.A.get()
            case 45:
                # sta mem[b]
                self.memory[self.B.get()] = self.A.get()
            case 46:
                # stb mem[arg]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[arg] = self.B.get()
            case 47:
                # stb mem[[arg]]
                self.ProgramCounter.increment()
                arg = self.memory[self.ProgramCounter.get()]
                self.memory[self.memory[arg]] = self.B.get()
            case 48:
                # stb mem[a]
                self.memory[self.A.get()] = self.B.get()


        self.ProgramCounter.increment()        
        self.updateMem()
