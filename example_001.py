from sys import stdout
import time

max = 100
for i in range(max):
    time.sleep(0.1)

    stdout.write(f'\r{(i + 1.0) / max:>6.1%} 終了しました。')
    stdout.flush()

print()