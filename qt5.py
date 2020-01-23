import visa

rm = visa.ResourceManager('c:/windows/system32/visa32.dll')
InfiniiVision = rm.open_resource("USB0::0x0957::0x179B::MY51452776::0::INSTR")
print(InfiniiVision.query('*IDN?'))


