import time

import RPi.GPIO as GPIO
import sendmail

GPIO.setmode(GPIO.BCM)

email_pin = 18
GPIO.setup(email_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buzzer_pin = 23
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    # Python2
    from Tkinter import *
    import Tkinter as tk
    from Tkinter.messagebox import showinfo
except ImportError:
    # Python3
    from tkinter import *
    import tkinter as tk
    from tkinter.messagebox import showinfo

hour = 12
minute = 0
alarmOn = False
buttonOn = False
buzzerOn = False
#ledOn = False

def tick(time1=''):
    global alarmOn
    global buzzerOn
    global buttonOn
    global ledOn
    # get the current local time from the PC
    actualTime = time.strftime('%H:%M:%S')
    
    #checks alarm time in order to display properly
    if minute <= 9:
        if hour <= 9:
            clockAlarm.config(text = "Alarm Time: 0{}:0{}".format(hour, minute))
        else: clockAlarm.config(text = "Alarm Time: {}:0{}".format(hour, minute))
    elif hour <= 9:
        clockAlarm.config(text = "Alarm Time: 0{}:{}".format(hour, minute))
    else:
        clockAlarm.config(text = "Alarm Time: {}:{}".format(hour, minute))

    #checks if its time to sound alarm if alarmOn is true
    if alarmOn:
        if minute <= 9:
            if hour <= 9:
                if (actualTime[:5] == "0{}:0{}".format(hour, minute)) and alarmOn:
                    activateAlarm()
            elif (actualTime[:5] == "{}:0{}".format(hour, minute)) and alarmOn:
                activateAlarm()
        elif hour <= 9:
            if (actualTime[:5] == "0{}:{}".format(hour, minute)) and alarmOn:
                    activateAlarm()
        else:
            if (actualTime[:5] == "{}:{}".format(hour, minute)) and alarmOn:
                activateAlarm()

    if buzzerOn:
        buzz(2000,.2)

    if buttonOn:
        input_state = GPIO.input(email_pin)
        if input_state == False:
            sendmail.send_email(email.get(), 'late', 'Dear '+name.get()+', \n\nI am sorry to say that I may be late today because '+reason.get()+'. I will be there ASAP. My apologies. \n\nSincerely, \n'+myName.get())
            showinfo('Email Sent','Late email has been sent! \nTime to wake up!')  
            snoozed()
            time.sleep(0.2)
    
    # if time string has changed, update it
    if actualTime != time1:
        time1 = actualTime
        clock.config(text=actualTime)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    clock.after(200, tick)
    
        
root = tk.Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack()

bottomframe2 = Frame(root)
bottomframe2.pack()

bottomframe3 = Frame(root)
bottomframe3.pack()

clock = tk.Label(frame, font=('times', 120, 'bold'), bg='white', padx=105, pady=25)
clockAlarm = tk.Label(frame, font=('times', 30, 'bold'), bg='grey')

clock.pack()
clockAlarm.pack()

def buzz(pitch, duration):
	period = 1.0 / pitch
	delay = period / 2
	cycles = int(duration * pitch)
	for i in range(cycles):
		GPIO.output(buzzer_pin, True)
		time.sleep(delay)
		GPIO.output(buzzer_pin, False)
		time.sleep(delay)

def increaseHour():
    global hour  
    if hour == 23:
        hour=0
    else:
        hour+=1

def decreaseHour():
    global hour  
    if hour == 0:
        hour=23
    else:
        hour-=1

def increaseMinute():
    global minute
    if minute == 55:
        increaseHour()
        minute = 0
    else:
        minute+=5

def decreaseMinute():
    global minute
    if minute == 0:
        decreaseHour()
        minute = 55
    else:
        minute-=5

def isAlarmActive():
    global alarmOn
    if alarmOn:
        alarmOn = False
        clockAlarm.config(bg = 'grey')
    else:
        alarmOn = True
        clockAlarm.config(bg = 'green')

def snoozed():
    global buttonOn
    global buzzerOn
    snooze.config(state="disabled")
    alarmActive.config(state="normal")
    addHour.config(state="normal")
    subHour.config(state="normal")
    addMinute.config(state="normal")
    subMinute.config(state="normal")
    buttonOn = False
    buzzerOn = False
    increaseMinute()
    isAlarmActive()
   
def activateAlarm():
    global buttonOn
    global buzzerOn
    isAlarmActive()
    alarmActive.config(state="disabled")
    addHour.config(state="disabled")
    subHour.config(state="disabled")
    addMinute.config(state="disabled")
    subMinute.config(state="disabled")
    clockAlarm.config(bg = 'red')
    snooze.config(state="normal")
    buttonOn = True
    buzzerOn = True
    
addHour = Button(bottomframe, text="Hour +", command=increaseHour)
addHour.pack(side = LEFT)

subHour = Button(bottomframe, text="Hour -", command=decreaseHour)
subHour.pack(side = LEFT)

addMinute = Button(bottomframe, text="Minute +", command=increaseMinute)
addMinute.pack(side = LEFT)

subMinute = Button(bottomframe, text="Minute -", command=decreaseMinute)
subMinute.pack(side = LEFT)

alarmActive = Button(bottomframe, text="Alarm on/off", command=isAlarmActive)
alarmActive.pack(side = LEFT)

snooze = Button(bottomframe, text="snooze", command=snoozed)
snooze.pack(side = LEFT)
snooze.config(state="disabled")

label = Label(bottomframe2, font=('times', 10, 'bold'), text="To (email):")
label.pack(side = LEFT)

email = Entry(bottomframe2)
email.pack(side = LEFT)
email.insert(10,"DEST. EMAIL")

label2 = Label(bottomframe2, font=('times', 10, 'bold'), text="Dear:")
label2.pack(side = LEFT)

name = Entry(bottomframe2)
name.pack(side = LEFT)
name.insert(10,"Boss")

label3 = Label(bottomframe3, font=('times', 10, 'bold'), text='I will be late because:')
label3.pack(side = LEFT)

reason = Entry(bottomframe3)
reason.pack(side = LEFT)
reason.insert(10,"I over slept")

label3 = Label(bottomframe3, font=('times', 10, 'bold'), text='Sincerely:')
label3.pack(side = LEFT)

myName = Entry(bottomframe3)
myName.pack(side = LEFT)
myName.insert(10,"YOUR NAME")

tick()
root.mainloop()
