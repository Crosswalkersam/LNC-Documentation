import time
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_range, strict_discrete_set

class LNC(Instrument):
    """Represents the SatDump LNC
    """
    def __init__(self, adapter, **kwargs):
        kwargs.update({"name": "SatDump X-Band LNC"})
        super().__init__(adapter, **kwargs)

    def write(self, command, **kwargs):
        """Write a string command to the instrument appending `write_termination`.

        :param command: command string to be sent to the instrument
        :param kwargs: Keyword arguments for the adapter.
        """
        self.adapter.write(command, **kwargs)
        time.sleep(1)

    run_state = Instrument.control(
        "PLL:STAT?",
        "PLL:STAT %s",
        "Turns the PLL output on/off",
        validator = strict_discrete_set,
        map_values = True,
        values = {"Active": 1, "Standby": 0, True: 1, False: 0}
    )

    frequency = Instrument.control(
        "PLL:FREQ?",
        "PLL:FREQ %s",
        "Sets the LO Frequency of the Converter",
        validator = strict_range,
        cast=int,
        values = (6.8e9, 8.3e9)
    )

    exernal_reference_frequency = Instrument.control(
        "REF:FREQ?",
        "REF:FREQ %s",
        "Sets the input frequency on the external reference port",
        validator = strict_range,
        cast=int,
        values = (10e6, 250e6)
    )

    identification = Instrument.measurement(
        "*IDN?",
        "Queries the instruments identification string"
    )

    lock_state = Instrument.measurement(
        "PLL:LOCK?",
        "Gets the lock state of the PLL",
        map_values=True,
        values={"Unlocked": 0, "Locked": 1}
    )
#Now we have the secret commands ==========================================================
    pll_power = Instrument.control(
        "228:PLL:POW?",
        "228:PLL:POW %s",
        "Controls the PLL output power",
        validator = strict_discrete_set,
        map_values=True,
        cast=int,
        values = {-5: 0, -1: 1, 2: 2, 5: 3}
    )

    chargepump_current = Instrument.control(
        "228:PLL:CPI?",
        "228:PLL:CPI %s",
        "Controls the PLL carge pump current",
        validator = strict_range,
        cast = int,
        map_values=True,
        values = {0.31: 0, 0.63: 1, 0.94: 2, 1.25: 3, 1.56: 4, 1.88: 5, 2.19: 6, 2.5: 7,
                  2.81: 8, 3.13: 9, 3.44: 10, 3.75: 11, 4.06: 12, 4.38: 13, 4.69: 14, 5: 15}
    )

    reference_divider = Instrument.control(
        "228:REF:DIV?",
        "228:REF:DIV %s",
        "Controls the reference divider",
        validator = strict_range,
        cast=int,
        values = (1, 1023)
    )

    integer_reg = Instrument.measurement(
        "228:PLL:INT?",
        "Returns the contents of the integer register",
        cast=int
    )

    fractional_reg = Instrument.measurement(
        "228:PLL:FRAC?",
        "Returns the contents of the integer register",
        cast=int
    )

    modulus_reg = Instrument.measurement(
        "228:PLL:MOD?",
        "Returns the contents of the integer register",
        cast=int
    )

    phasedetector_frequency = Instrument.measurement(
        "228:PLL:FPFD?",
        "Returns the contents of the integer register",
        cast=int
    )

    channelspacing = Instrument.measurement(
        "228:PLL:CHSP?",
        "Returns the contents of the integer register",
        cast=int
    )

    RF_divider = Instrument.measurement(
        "228:PLL:RFDV?",
        "Returns the contents of the integer register",
        cast=int,
        map_values=True,
        values={1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6}
    )

    def sanitycheck(self):
        """Queries all values via UART and cross-checks them with each other.
        """
        if self.phasedetector_frequency * self.integer_reg != self.frequency / 2:
            return -1
        if self.exernal_reference_frequency / self.reference_divider != self.phasedetector_frequency:
            return -1
        if self.channelspacing != self.phasedetector_frequency:
            return -1
        if self.fractional_reg != 0:
            return -1
        if self.modulus_reg != 1:
            return -1
        return 1
