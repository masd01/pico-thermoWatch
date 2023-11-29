import machine
import ssd1306
import time
from machine import ADC

#set up on board thermo sensor
sensor_temp = ADC(4) 
conversion_factor = 3.3 / (65535)

#set up oled display
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#set up buttons
button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

#initialize variables
hours = 0
minutes = 0
seconds = 0
days = 0
months = 0
years = 2020
times1 = 0

#function to update the time
def update_time():
    global hours, minutes, seconds
    seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
            if hours == 24:
                hours = 0

#function to update date
def update_date():
    global years, months, days
    days += 1
    if days == 31:
        days = 0
        months += 1
        if months == 12:
            months = 0
            years += 1

#main loop
while True:
    #get temperature    
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    tstring=str(temperature)

    #check if button 1 is pressed
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
            oled.fill(0)
            oled.text('Set',0,0)
            oled.text('Day',0,20)
            oled.show()
            time.sleep(1)
        elif times1 == 4:
            oled.fill(0)
            oled.text('Set',0,0)
            oled.text('Month',0,20)
            oled.show()
            time.sleep(1) 
        elif times1 == 5:
            oled.fill(0)
            oled.text('Set',0,0)
            oled.text('Year',0,20)
            oled.show()
            time.sleep(1)
        elif times1 == 6:
            times1 = 0
            oled.fill(0)
            oled.text('masd',46,20) # that's me :)
            oled.show()
            time.sleep(1)

    #check if button 2 is pressed
    if not button2.value():
        if times1 == 1:
            hours += 1
            if hours == 24:
                hours = 0
            update_time()
            oled.fill(0)
            oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
            oled.show()
            time.sleep(1)
        elif times1 == 2:
            minutes += 1
            if minutes == 60:
                minutes = 0
            update_time()
            oled.fill(0)
            oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
            oled.show()
            time.sleep(1)
        elif times1 == 3:
            days += 1
            if days == 32:
                days = 1
            oled.fill(0)
            oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
            oled.show()
            time.sleep(1)
        elif times1 == 4:
            months += 1
            if months == 13:
                months = 1
            oled.fill(0)
            oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
            oled.show()
            time.sleep(1)
        elif times1 == 5:
            years += 1            
            oled.fill(0)
            oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
            oled.show()
            time.sleep(1)

    update_time()
#   update_date()
    oled.fill(0)
    oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
    oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
    oled.text('Temp: '+ tstring,0,40)
    oled.show()
    time.sleep(1)
   
