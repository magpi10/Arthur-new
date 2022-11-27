import datetime
import update
import RPi.GPIO as GPIO
from time import sleep, mktime
import search

url = "https://spotthestation.nasa.gov/sightings/xml_files/South_Africa_None_Johannesburg.xml"
led = 14
buzzer = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

update.update_xml(url)

while True:
    next_pass = update.update_next_pass()

    time_allowance = datetime.timedelta(seconds=1)

    if next_pass[0] == "":
        last_update = update.last_updated_check()

        now_unix = mktime(datetime.datetime.now().timetuple())
        last_update_unix = mktime(last_update.timetuple())

        time_to_next_update = 1209600 - (now_unix - last_update_unix)

        print(str(time_to_next_update), f"at {datetime.datetime.now()}")
        sleep(time_to_next_update)
        update.update_xml(url)
        continue

    if not (datetime.datetime.now() - time_allowance) <= next_pass[0] <= (datetime.datetime.now() + time_allowance):
        now_unix = mktime(datetime.datetime.now().timetuple())
        next_pass_unix = mktime(next_pass[0].timetuple())
        time_to_next_pass = next_pass_unix - now_unix

        print(str(time_to_next_pass),  f"at {datetime.datetime.now()}")
        sleep(time_to_next_pass)

    now = datetime.datetime.now()
    min_time = datetime.datetime(now.year, now.month, now.day, 9, 0, 0, 0)
    max_time = datetime.datetime(now.year, now.month, now.day, 21, 0, 0, 0)

    print(f"The ISS is above you at {now}")

    if min_time < now < max_time:
        print("Shouting")
        dur = next_pass[1]
        for i in range(0, dur):
            GPIO.output(led, GPIO.HIGH)
            if i < 10:
                GPIO.output(buzzer, GPIO.HIGH)
            sleep(0.10)
            GPIO.output(buzzer, GPIO.LOW)
            sleep(0.40)
            GPIO.output(led, GPIO.LOW)

            sleep(0.50)

    else:
        print("Keeping Quiet")
