import machine
import ssd1306
import time
from machine import ADC, Pin, I2C

# Temperature sensor (Pico's internal)
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

# OLED display (128x64)
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttons (PULL_UP: pressed = 0, released = 1)
button1 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)

# --- Time/Date Variables ---
hours, minutes, seconds = 0, 0, 0
days, months, years = 1, 1, 2020
times1 = 0  # Menu state
last_update = time.ticks_ms()  # For precise timing

# --- Helper Functions ---
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_days_in_month(month, year):
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    else:
        return 31

def update_time():
    global hours, minutes, seconds, days, months, years
    seconds += 1
    if seconds >= 60:
        seconds = 0
        minutes += 1
        if minutes >= 60:
            minutes = 0
            hours += 1
            if hours >= 24:
                hours = 0
                update_date()  # Update date when day changes!

def update_date():
    global days, months, years
    days += 1
    if days > get_days_in_month(months, years):
        days = 1
        months += 1
        if months > 12:
            months = 1
            years += 1

# --- Main Loop ---
while True:
    current_time = time.ticks_ms()
    
    # Update time every 1000ms (1 second)
    if time.ticks_diff(current_time, last_update) >= 1000:
        update_time()
        last_update = current_time
        
        # Read temperature
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        tstring = "{:.2f}°C".format(temperature)
        
        # Display time, date, and temperature
        oled.fill(0)
        oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
        oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
        oled.text("Temp: " + tstring, 0, 40)
        oled.show()
    
    # Button 1: Cycle through menu options
    if not button1.value():
        times1 = (times1 + 1) % 6  # Wrap around after 5
        oled.fill(0)
        menu_options = ["Set Hours", "Set Minutes", "Set Day", "Set Month", "Set Year"]
        if times1 < 5:
            oled.text(menu_options[times1], 0, 20)
        else:
            oled.text("Ready!", 46, 20)
        oled.show()
        time.sleep(0.3)  # Debounce delay
    
    # Button 2: Adjust selected value
    if not button2.value():
        if times1 == 0:  # Hours
            hours = (hours + 1) % 24
        elif times1 == 1:  # Minutes
            minutes = (minutes + 1) % 60
            seconds = 0  # Reset seconds when adjusting minutes
        elif times1 == 2:  # Day
            days = (days % get_days_in_month(months, years)) + 1
        elif times1 == 3:  # Month
            months = (months % 12) + 1
        elif times1 == 4:  # Year
            years += 1
        
        # Update display immediately after adjustment
        oled.fill(0)
        oled.text("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), 0, 0)
        oled.text("{:02d}/{:02d}/{:04d}".format(days, months, years), 0, 20)
        oled.show()
        time.sleep(0.3)  # Debounce delay
