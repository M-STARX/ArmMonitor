# Arm Monitor - Year in Review
Authored by Vihaan Dutta
(2024-2025 Arm Monitor Subteam Lead, 2025-2026 Programming Director)

## Year Summary

For the 2024-2025 season, the Arm Monitor team opted to move away from the last year's design to decrease the size of the device and enable the device to have more functionality. The previous design was comprised of a Raspberry Pi, a 6-8 inch Pi HAT display (see the box labeled "Old Arm Monitor" in the storage closet), a power bank to power to Raspberry Pi/Display, and a housing for all the components. Veteran members instructed the Arm Monitor team to reduce the size of the Arm Monitor for the 2024-2025 season to reduce its clunkiness. As the previous design utilized components which were inherently large, such as the Raspberry Pi single-board computer, the team decided to redesign the Arm Monitor from scratch.

## Overall Recommendations for the 2025-2026 Arm Monitor Team

Hey everyone, this is Vihaan.

I will be your main point of contact for help on the Arm Monitor as I was the Arm Monitor subteam lead for the 2024-2025 season. On a typical day, I will come at the beginning of the meeting to speak to you all about what you all will be working on for the day. At the end of the meeting, I'll come back again to inquire about progress. You all will spend the majority of time in M-STARX in these Sunday meetings, but the Arm Monitor lead should create meetings between team members throughout the week as needed to ensure steady progress. Side note for the 2025-2026 Arm Monitor lead, make sure to take attendance on Slack before you leave each meeting.

For this year, I'd recommend you all stick to the same hardware we used last time (specifically, the Raspberry Pi Pico 2 and ILI9341 display). We spent a great amount of time picking the most appropriate device, researching how to upload code to it, how to interface it with the display, creating the wiring for the devices, etc. Your overall goal is to take the hardware setup from last year and figure out communication between the Arm Monitor's Raspberry Pi Pico 2 and the Raspberry Pi 4/the Moteus HAT's data on the exoskeleton. We primarily attempted implementing the UART communication protocol last year for these communications (I2C and SPI require a master/slave relationship, but we wanted a 2-way communication so we believed a setup with these protocols were impossible), but ultimately did not have enough time to get it to work (see [communications.md](communications.md) for our documentation on between-pi device communications). We were also unable to create a setup to power the Arm Monitor from the exoskeleton battery. This season's Fall semester should be spent perfecting the communication such that the Arm Monitor can read and modify information on the exoskeleton computer (see battery values, switch algorithms, modify feed-forward torque values, etc.). Subsequently, the Winter semester should be spent testing the Arm Monitor with the exoskeleton (assuming the exoskeleton is functional in the Winter). Essentially:

1. Establish wired communication between the exoskeleton and arm monitor (bluetooth was very unreliable the previous year)
2. Enable read and write between the exoskeleton and arm monitor
3. Power the Arm Monitor with the exoskeleton battery
4. Test the Arm Monitor

This list is not a golden rule the team needs to follow, but based on my experience I believe this is a good path of action.

## Choice of Computing Board

Instead of using a single-board computer, the team opted to use a microcontroller because they require less power to function, the boot time is faster, and overall costs less (see the ["Arm Monitor - Preliminary Design Review" slides](https://docs.google.com/presentation/d/1sFb4J-veF4RQxm-2h88zRkpuaaTNrBoXynaoWEgADPU/edit?usp=sharing)).

The team researched the Teensy 4.1, Raspberry Pi Pico 2, and STM Nucleo 32, but ultimately chose the Raspberry Pi Pico 2 primarily due to team experience. 3x of these devices were purchased (see the box labeled "Arm Monitor" in the storage closet).

## Choice of Display

The team's goal was to select a display that was cost-effective, smaller, compatible, quality, and used the least number of GPIO pins on the Raspberry Pi Pico 2. We discovered the HiLetgo ILI9341 2.8" SPI LCD display fit all of these criteria and purchased one of them (see the box labeled "Arm Monitor" in the storage closet). Summary of its specifications are on the ["Arm Monitor - Preliminary Design Review" slides](https://docs.google.com/presentation/d/1sFb4J-veF4RQxm-2h88zRkpuaaTNrBoXynaoWEgADPU/edit?usp=sharing).

To interact with the display, the team decided to use a single rotary encoder. This would enable switching between screens on the Arm Monitor to see different information, as well as modifying values (feed-forward torque, for example).

## Choice of Battery

Even with our changes in the computing board and choice of display, our team discovered the battery took up the most space in the design of the Arm Monitor. Because of this, we decided it would be optimal to power the Pico with the battery on the exoskeleton to reduce the space it takes.

## Choice of Programming Language

We used MicroPython on the Arm Monitor's Raspberry Pi Pico 2.