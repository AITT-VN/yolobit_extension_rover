# Mục mở rộng dành cho bộ kit xe điều khiển Rover

```python
from rover import *
import time

if True:
  rover.show_rgb_led(0, hex_to_rgb("#33ccff"))
  rover.show_led(1, 1) # left led
  rover.show_led(2, 1) # right led

while True:
  print(rover.ultrasonic.distance_cm())
  time.sleep_ms(100)
```
