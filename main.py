import machine
import ssd1306
import time
from machine import ADC

# Set up on-board thermo sensor
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

# Set up OLED display
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Set up buttons
button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

# Initialize variables
hours = 0
minutes = 0
seconds = 0
days = 1
months = 1
years = 2020
times1 = 0

# Function to determine if a year is a leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Function to get the number of days in a month
def get_days_in_month(month, year):
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    else:
        return 31

# Function to update the time
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

# Function to update the date
def update_date():
    global years, months, days
    days += 1
    if days > get_days_in_month(months, years):
        days = 1
        months += 1
        if months > 12:
            months = 1
            years += 1

# Main loop
while True:
    # Get temperature    
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    tstring = "{:.2f}".format(temperature)

    # Check if button 1 is pressed
    if not button1.value():
        times1 += 1
        oled.fill(0)
        if times1 == 1:
            oled.text('Set Hours', 0, 20)
        elif times1 == 2:
            oled.text('Set Minutes', 0, 20)
        elif times1 == 3:
            oled.text('Set Day', 0, 20)
        elif times1 == 4:
            oled.text('Set Month', 0, 20)
        elif times1 == 5:
            oled.text('Set Year', 0, 20)
        elif times1 == 6:
            times1 = 0
            oled.text('masd', 46, 20)  # that's me :)
        oled.show()
        time.sleep(1)

    # Check if button 2 is pressed
    if not button2.value():
        if times1 == 1:
            hours = (hours + 1) % 24
            update_time()
        elif times1 == 2:
            minutes = (minutes + 1) % 60
            update_time()
        elif times1 == 3:
            days = (days % get_days_in_month(months, years)) + 1
        elif times1 == 4:
            months = (months % 12) + 1
        elif times1 == 5:
            years += 1
        
        oled.fill(0)
        oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
        oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
        oled.show()
        time.sleep(1)

    update_time()
    oled.fill(0)
    oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
    oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
    oled.text('Temp: ' + tstring, 0, 40)
    oled.show()
    time.sleep(1)
