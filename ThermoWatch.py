# Import necessary libraries
import machine
import ssd1306
import time
import utime
from machine import ADC

#initialize sensor
sensor_temp = ADC(4) 
conversion_factor = 3.3 / (65535)

# Set up the OLED display
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Set up the buttons
button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

# Initialize variables
hours = 0
minutes = 0
seconds = 0
#days = 0
#months = 0
#years = 0
times1 = 0

# Function to update the time
def update_time():
    global hours, minutes, seconds, days, months, years
    seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
            if hours == 24:
                hours = 0

# Main loop
while True:
    #get temperature    
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    tstring=str(temperature)

    # Check if button 1 is pressed
    if not button1.value():
        times1 += 1
        if times1 == 1:
            oled.fill(0)
            oled.text('Set',0,0)
            oled.text('Hours',0,20)
            oled.show()
            time.sleep(1)
        elif times1 == 2:
            oled.fill(0)
            oled.text('Set',0,0)
            oled.text('Minutes',0,20)
            oled.show()
            time.sleep(1)
        elif times1 == 3:
            times1 = 0
            oled.fill(0)
            oled.text('masd',46,20)
            oled.show()
            time.sleep(1)
#        elif times1 == 4:           
#            oled.fill(0)
#            oled.text('Set',0,0)
#            oled.text('Day',0,20)
#            oled.show()
#            time.sleep(1)
#        elif times1 == 5:
#            oled.fill(0)
#            oled.text('Month',0,40)
#            oled.show()
#            utime.sleep(1)
#        elif times1 == 6:
#            oled.fill(0)
#            oled.text('Year',0,40)
#            oled.show()
#            utime.sleep(1)

    # Check if button 2 is pressed
    if not button2.value():
        if times1 == 1:
            hours += 1
            if hours == 24:
                hours = 0
            update_time()
            oled.fill(0)
            oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
            oled.show()
            time.sleep(0.1)
        elif times1 == 2:
            minutes += 1
            if minutes == 60:
                minutes = 0
            update_time()
            oled.fill(0)
            oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
            oled.show()
            time.sleep(0.1)
#        elif times1 == 3:
#            day += 1            
#            oled.fill(0)
#            oled.text("{:02d}/{:02d}/{}".format(utime.localtime()[2], utime.localtime()[1], utime.localtime()[0]), 0, 20)
#            oled.show()
#            utime.sleep(1)

    # Update the time
    update_time()

    # Clear the display
    oled.fill(0)

    # Display the time
    oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)

    # Display the date
    oled.text("{:02d}/{:02d}/{}".format(utime.localtime()[2], utime.localtime()[1], utime.localtime()[0]), 0, 20)
    
    # Display temperature
    oled.text('Temp: '+ tstring,0,40)

    # Show the display
    oled.show()

    # Delay for 1 second
    utime.sleep(1)
    