## Overview
A simple connector PCB was designed and ordered for the 2025-2026 version of the Arm Monitor. This branch contains the Altium project for the PCB (PCB folder) as well as the 3D-printed case (Case folder).

## PCB
The PCB built in Altium is located in this folder. Multiple artifacts of the original wired implementation exist, in particular the 3 pin right angle JST connector that was meant for UART communications. The XT30, which is directly connected to the power/ground planes of the board was originally meant to wired into the exo, but as a stop gap, the LiPo battery placed into the case provides independent power.

| Part    | Description |
| ----------- | ----------- |
| Raspberry Pi Pico 2W      | Microcontroller       |
| ILI9341 SPI Display   |  Main Display       |
| 5x Switches | Mode Switching Buttons and User Control|
| TP4056 + 3V LiPo Battery | Maintain Power Independence from the Exo |
| XT30 + 3 Pin Right Angle JST | Artifacts of the Original Wired Implementation|
| Mini Speaker + PAM8302 Mono Amplifier | Unimplemented Speaker System |  

![Altium Image of the PCB](/PCBImage.png)
## Case
A 3D printed case is located in the case folder in the form of a .step file as well as a Fusion Archive file. 

A power switch as added in the hole below the screen. The Lipo battery is situated along with the TP4056 charging module in the interior of the case, and a wire with an xt30 connector can be wired out of the hole and into the xt30 connector on the PCB to provide power.

![Fusion 360 Image of the Case](/FusionImage.png)

