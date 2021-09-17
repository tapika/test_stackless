import stackless
import time

print('-> test2')

for i in range(3):
    print(i+1)
    stackless.schedule()

print('<- test2')
