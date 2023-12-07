import time
import datetime
for x in range(0,100):
    time.sleep(5)
    print(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

