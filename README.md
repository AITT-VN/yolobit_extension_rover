# Thư viện mở rộng cho bộ kit xe điều khiển car:bit v2

```python
from carbitv2 import *
from carbitv2_hcsr04 import *
from carbitv2_ble_uart_peripheral import *
import time

def ble_on_rx_callback(event):
  if event == (!B516):
    carbit.forward(0)
  elif event == (!B615):
    carbit.backward(0)
  elif event == (!B714):
    carbit.left(0)
  elif event == (!B714):
    carbit.right(0)
  else:
    carbit.stop()

ble_start('carbit')
ble_on_rx(ble_on_rx_callback)

if True:
  carbit.show_rgb_led(0, hex_to_rgb("#33ccff"))
  carbit.show_led(1, 1) # left led
  carbit.show_led(2, 1) # right led

while True:
  print(ultrasonic.distance_cm())
  time.sleep_ms(100)
```
