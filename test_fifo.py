from fifo_manager import FIFOManager
fm = FIFOManager('D2E', 'w')
fm.write('{"task":"query"}', 5)
fm1 = FIFOManager('E2D', 'r')
print("before read")
print(fm1.read())
print("after read")
