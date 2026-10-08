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

## Cân chỉnh để xe đi thẳng

Tỉ lệ tốc độ trái/phải được lưu vào bộ nhớ robot (`config.json`): **giữ nguyên khi nạp code mới, chỉ bị xóa khi nạp lại firmware**. Mỗi lần khởi động, rover tự đọc lại tỉ lệ đã lưu.

Dùng block "lưu tỉ lệ tốc độ trái ... phải ... vào bộ nhớ" hoặc code:

```python
from rover import *

rover.save_speed_ratio(1, 0.95)  # lưu vào bộ nhớ, giữ khi nạp code mới
rover.speed_ratio(1, 0.95)       # chỉ dùng tạm đến khi khởi động lại
print(rover.get_speed_ratio())
```

Lưu `rover.save_speed_ratio(1, 1)` để trở về mặc định.
