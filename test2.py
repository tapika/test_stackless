import stackless
import time
from pathlib import Path

print('-> test2')

p = Path('.')
print([x for x in p.iterdir() if x.is_dir()])

for i in range(3):
    print(i+1)
    stackless.schedule()

print('<- test2')
