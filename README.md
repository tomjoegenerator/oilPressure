# oilPressure

This program was written as an add-on enhancement for use with the Genmon backup generator monitoring program (https://github.com/jgyates/genmon/wiki). It will read the generator engine’s oil pressure and display it on the Genmon “Monitor” page. Monitoring the oil pressure is important since high oil pressure could indicate clogged oil flow and low oil pressure could indicate low oil volume. Most generators only provide a low oil pressure engine cut-off which shuts down the generator at the critical point, no warning that problems are developing. Knowing in advance that problems may be developing is important, especially in a generator used for emergency power.

The oilPressure.py program is written python it reads a MCP3008 ADC via the spi bus.  The spi bus was chosen after experimenting with the i2c bus and finding that when the generator started there was too much noise causing read errors.  We tried to incorporate a filter, but it proved to be too unreliable.   After reading the ADC the value is converted to a voltage and ten converted to an oil pressure using a power fit.  In order to determine what type of fit we pressurized the sensor with air and measured the voltage.  We tried a linear, quadric, and a power fit.  WE felt the power fit was best, the comparison of the fits can be view in the Various Fit pdf file included here.  Finally the oil pressure is written out to a userdefined.json fillet be read into the gencon program and displayed on the Monitor page.  Our hope is if people find this useful, a gauge can be incorporated in the genmon program.

Having the oil pressure sending unit isolated from ground helps prevent interference on the data line so a VDO #360-410, 0 – 80 PSI sending unit was chosen. This sending unit is teed off of the engine’s oil system where the factory, low oil pressure switch is located. Adafruit’s documentation of the MCP3008 was invaluable in figuring out the circuitry and developing the code. The circuitry was built on a piece of printed circuit board and connects to the GPIO pins on the Pi.

Parts list:

Adafruit:
https://www.adafruit.com/

MCP3008 10-Bit ADC With SPI Interface Product ID #856
Assorted Pi GPIO headers, hardware & connectors

ebay:
https://www.ebay.com/

VDO #360-410 Pressure Sender Unit 0 – 80 PSI, 10 – 180 ohms
Double Sided Prototype Printed Circuit Board
1,000-ohm resistor







