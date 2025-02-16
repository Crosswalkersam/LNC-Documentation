from lnc import LNC

downconverter = LNC('COM3')
#downconverter.run_state = False
downconverter.frequency = 7800000000
#downconverter.exernal_reference_frequency = 10000000

print("######### Device summary #########")
print(f"LO Frequency: {downconverter.frequency / 1e9}GHz")
print(f"Reference Frequency: {downconverter.exernal_reference_frequency / 1e6}MHz")
print(f"LO Power: {downconverter.pll_power}dBm")
print(f"Lock status: {downconverter.lock_state}")
print(f"Power status: {downconverter.run_state}")
print(f"Charge pump current: {downconverter.chargepump_current}mA")
print(f"Reference divider: {downconverter.reference_divider}")
print(f"Phasedetector frequency: {downconverter.phasedetector_frequency / 1e6}MHz")
print(f"Channelspacing: {downconverter.channelspacing / 1e6}MHz")
print(f"RF divider: {downconverter.RF_divider}")
print(f"Integer value: {downconverter.integer_reg}")
print(f"Fractional value: {downconverter.fractional_reg}")
print(f"Modulus value: {downconverter.modulus_reg}")

if downconverter.sanitycheck():
    print("All okay!")
else:
    raise ValueError
