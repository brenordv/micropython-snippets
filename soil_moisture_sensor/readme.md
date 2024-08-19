# Soil Moisture Monitor
This project is a soil moisture monitor that uses a Raspberry Pi Pico and a soil moisture sensor to monitor 
the moisture level of a plant. 

Right now it doesn't do much, but it calculates the percentage of moisture in the soil and prints it to the
serial console.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico
- Capacitive Soil Moisture 1.2 (KYES516)

> Didn't find a datasheet for this sensor and pinout is pretty straight forward. 
> Connect the VCC to 3.3V, GND to GND, and the signal pin to GP26 (Pico) or some other ADC pin.

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

## Example output
```text
>>> %Run -c $EDITOR_CONTENT

MPY: soft reboot
Sensor warming up...
Soil Moisture: 97.46%
Soil Moisture: 97.31%
Soil Moisture: 97.97%
Soil Moisture: 97.06%
Soil Moisture: 97.31%
Soil Moisture: 97.77%
Soil Moisture: 97.67%
Soil Moisture: 97.51%
Soil Moisture: 97.92%
Soil Moisture: 97.31%
Soil Moisture: 97.26%
Soil Moisture: 97.11%
Soil Moisture: 97.72%
Soil Moisture: 97.06%
Soil Moisture: 97.92%
Soil Moisture: 97.26%
Soil Moisture: 97.16%
Soil Moisture: 97.46%
Soil Moisture: 97.67%
Soil Moisture: 98.33%
Soil Moisture: 97.67%
Soil Moisture: 97.61%
Soil Moisture: 97.67%
Soil Moisture: 96.96%
Soil Moisture: 97.87%
Soil Moisture: 98.07%
Soil Moisture: 96.96%
Soil Moisture: 97.77%
Soil Moisture: 97.51%
Soil Moisture: 97.31%
Soil Moisture: 97.21%
Soil Moisture: 97.97%
Soil Moisture: 97.97%
Soil Moisture: 97.26%
Soil Moisture: 97.11%
Soil Moisture: 97.11%
Soil Moisture: 96.75%
Soil Moisture: 97.56%
Soil Moisture: 97.21%
Soil Moisture: 98.38%
Soil Moisture: 98.38%
Soil Moisture: 97.21%
Soil Moisture: 96.96%
Soil Moisture: 97.31%
Soil Moisture: 97.92%
Soil Moisture: 97.36%
Soil Moisture: 97.46%
Soil Moisture: 97.72%
Soil Moisture: 96.85%
Soil Moisture: 97.36%
Soil Moisture: 97.21%
Soil Moisture: 97.61%
Soil Moisture: 98.58%
Soil Moisture: 97.67%
Soil Moisture: 97.06%
```