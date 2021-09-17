import stackless
import time

print('-> test1')
#time.sleep(0.5)
stackless.schedule()
time.sleep(0.01)
#stackless.schedule()
#time.sleep(0.5)
#stackless.schedule()
#time.sleep(0.5)
stackless.schedule()
#time.sleep(0.5)
print('<- test1')

