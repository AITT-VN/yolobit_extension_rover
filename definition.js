
Blockly.Blocks['carbitv2_move'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_move",
        "message0": "%1 di chuyển %2 với tốc độ %3 (0-100)",
        "args0": [
          {
            "type": "field_image",
            "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/move.svg",
            "width": 20,
            "height": 20,
            "alt": "",
            "flipRtl": false
          },
          {
            "type": "field_dropdown",
            "name": "direction",
            "options": [
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-up.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "forward"
              ],
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-down.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "backward"
              ],
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-left.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "turn_left"
              ],
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-right.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "turn_right"
              ]
            ]
          },
          {
            min: 0,
            type: "input_value",
            check: "Number",
            value: 50,
            name: "speed",
          }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python["carbitv2_move"] = function (block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var dir = block.getFieldValue("direction");
  var speed = Blockly.Python.valueToCode(block, 'speed', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = "carbit." + dir + "(" + speed + ")\n";
  return code;
};

Blockly.Blocks['carbitv2_move_delay'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_move_delay",
        "message0": "%1 di chuyển %2 với tốc độ %3 (0-100) trong %4 giây",
        "args0": [
          {
            "type": "field_image",
            "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/move.svg",
            "width": 20,
            "height": 20,
            "alt": "",
            "flipRtl": false
          },
          {
            "type": "field_dropdown",
            "name": "direction",
            "options": [
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-up.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "forward"
              ],
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-down.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "backward"
              ],
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-left.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "turn_left"
              ],
              [
                {
                  "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-right.svg",
                  "width": 15,
                  "height": 15,
                  "alt": "*"
                },
                "turn_right"
              ]
            ]
          },
          {
            min: 0,
            type: "input_value",
            check: "Number",
            value: 50,
            name: "speed",
          },
          {
            min: 0,
            type: "input_value",
            check: "Number",
            name: "time",
          }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python["carbitv2_move_delay"] = function (block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var dir = block.getFieldValue("direction");
  var speed = Blockly.Python.valueToCode(block, 'speed', Blockly.Python.ORDER_ATOMIC);
  var time = Blockly.Python.valueToCode(block, 'time', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = "carbit." + dir + "(" + speed + ", " + time + ")\n";
  return code;
};

Blockly.Blocks['carbitv2_move_motor'] = {
  init: function() {
    this.jsonInit(
    {
        "type": "carbitv2_move_motor",
        "message0": "%3 quay động cơ trái tốc độ %1 động cơ phải %2 (-100 đến 100)",
        "args0": [
          {
            "type": "input_value",
            "name": "left_wheel_speed",
            "check": "Number",
        },
        {
            "type": "input_value",
            "name": "right_wheel_speed",
            "check": "Number",
        },
        {
            "type": "field_image",
            "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/motor.svg",
            "width": 20,
            "height": 20,
            "alt": "*",
            "flipRtl": false
        }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python["carbitv2_move_motor"] = function (block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var left_wheel_speed = Blockly.Python.valueToCode(block, 'left_wheel_speed', Blockly.Python.ORDER_ATOMIC);
  var right_wheel_speed = Blockly.Python.valueToCode(block, 'right_wheel_speed', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = "carbit.set_wheel_speed(" + left_wheel_speed + ", " + right_wheel_speed + ")\n";
  return code;
};

Blockly.Blocks['carbitv2_stop'] = {
  init: function() {
    this.jsonInit({
        "type": "carbitv2_stop",
        "message0": "%1 dừng di chuyển",
        "args0": [
            {
            "type": "field_image",
            "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/stop.svg",
            "width": 20,
            "height": 20,
            "alt": "*",
            "flipRtl": false
            }],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
    });
  }
};


Blockly.Python["carbitv2_stop"] = function (block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  // TODO: Assemble Python into code variable.
  var code = "carbit.stop()\n";
  return code;
};

Blockly.Blocks['carbitv2_show_led'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_show_led",
        "message0": "%2 đèn %1 ",
        "args0": [
          {
            "type": "field_dropdown",
            "name": "led",
            "options": [
              [
                "cả hai bên",
                "0"
              ],
              [
                "trái",
                "1"
              ],
              [
                "phải",
                "2"
              ]
            ]
          },
          {
            "type": "field_dropdown",
            "name": "state",
            "options": [
              [
                "bật",
                "1"
              ],
              [
                "tắt",
                "0"
              ]
            ]
          }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
      );
    }
  };

Blockly.Python['carbitv2_show_led'] = function(block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var dropdown_led = block.getFieldValue('led');
  var dropdown_state = block.getFieldValue('state');
  // TODO: Assemble Python into code variable.
  var code = 'carbit.show_led(' + dropdown_led +', ' + dropdown_state + ')\n';
  return code;
};

Blockly.Blocks['carbitv2_show_rgb_led'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_show_rgb_led",
        "message0": "đổi led RGB số %1 thành màu %2",
        "args0": [
          {
            "type": "input_value",
            "name": "number_led"
          },
          {
            "type": "input_value",
            "name": "color"
          }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
      );
    }
  };

Blockly.Python['carbitv2_show_rgb_led'] = function(block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var value_number_led = Blockly.Python.valueToCode(block, 'number_led', Blockly.Python.ORDER_ATOMIC);
  var value_color = Blockly.Python.valueToCode(block, 'color', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'carbit.show_rgb_led(' + value_number_led +', hex_to_rgb(' + value_color +'))\n';
  return code;
};

Blockly.Blocks['carbitv2_show_rgb_led_all'] = {
  init: function() {
    this.jsonInit({
      "type": "carbitv2_show_rgb_led_all",
      "message0": "đổi màu tất cả led RGB thành %1",
      "args0": [
        {
          "type": "input_value",
          "name": "color"
        }
      ],
      "inputsInline": true,
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#cb2026",
      "tooltip": "",
      "helpUrl": ""
    }
    );
  }
};

Blockly.Python['carbitv2_show_rgb_led_all'] = function(block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var value_color = Blockly.Python.valueToCode(block, 'color', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'carbit.show_rgb_led(0, hex_to_rgb(' + value_color +'))\n';
  return code;
};

Blockly.Blocks['carbitv2_ultrasonic_read'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_ultrasonic_read",
        "message0": "%1 đọc cảm biến khoảng cách (cm)",
        "args0": [
          {
            "type": "field_image",
            "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/ultrasonic.png",
            "width": 20,
            "height": 20,
            "alt": "*",
            "flipRtl": false
          }
        ],
        "colour": "#cb2026",
        "output": "Number",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python["carbitv2_ultrasonic_read"] = function (block) {
  Blockly.Python.definitions_['import_carbitv2_ultrasonic'] = 'from carbitv2_hcsr04 import *';
  // TODO: Assemble Python into code variable.
  var code = "ultrasonic.distance_cm()";
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['carbitv2_ultrasonic_detect'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_ultrasonic_detect",
        "message0": "%1 đọc cảm biến khoảng cách %2 %3 cm %4",
        "args0": [
          {
            "type": "field_image",
            "src": "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/ultrasonic.png",
            "width": 20,
            "height": 20,
            "alt": "*",
            "flipRtl": false
          },
          {
            "type": "field_dropdown",
            "name": "compare",
            "options": [
              ["<", "<"],
              [">", ">"],
              ["=", "=="],
            ],
          },
          {
            "type": "input_value",
            "name": "distance"
          },        
          {
            type: "input_dummy",
          }
        ],
        "colour": "#cb2026",
        "output": "Boolean",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python["carbitv2_ultrasonic_detect"] = function (block) {
  Blockly.Python.definitions_['import_carbitv2_ultrasonic'] = 'from carbitv2_hcsr04 import *';
  var compare = block.getFieldValue("compare");
  var value_distance = Blockly.Python.valueToCode(block, 'distance', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = "ultrasonic.distance_cm() " + compare + " "+ value_distance;
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['carbitv2_line_sensor_check'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_line_sensor_check",
        "message0": "đọc cảm biến line %1 %2 %3",
        "args0": [
          {
            "type": "field_dropdown",
            "name": "NAME",
            "options": [
              [
                "trái",
                "pin0"
              ],
              [
                "phải",
                "pin1"
              ]
            ]
          },
          {
            "type": "field_dropdown",
            "name": "COMPARE",
            "options": [
              [
                "<",
                "<"
              ],
              [
                ">",
                ">"
              ]
            ]
          },
          {
            "type": "input_value",
            "name": "num"
          }
        ],
        "inputsInline": true,
        "output": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python['carbitv2_line_sensor_check'] = function(block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var dropdown_name = block.getFieldValue('NAME');
  var dropdown_compare = block.getFieldValue('COMPARE');
  var value_name = Blockly.Python.valueToCode(block, 'num', Blockly.Python.ORDER_ATOMIC);
  var code = dropdown_name + '.read_analog() ' + dropdown_compare + ' ' + value_name;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['carbitv2_line_sensor_read'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_line_sensor_read",
        "message0": "đọc giá trị cảm biến line %1",
        "args0": [
          {
            "type": "field_dropdown",
            "name": "NAME",
            "options": [
              [
                "trái",
                "pin0"
              ],
              [
                "phải",
                "pin1"
              ]
            ]
          }
        ],
        "output": null,
        "colour": "#cb2026",
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};

Blockly.Python['carbitv2_line_sensor_read'] = function(block) {
  Blockly.Python.definitions_['import_carbitv2'] = 'from carbitv2 import *';
  var dropdown_name = block.getFieldValue('NAME');
  var code = dropdown_name + '.read_analog()';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['carbitv2_stringtonumber'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "carbitv2_stringtonumber",
        "message0": "đổi chữ thành số %1",
        "args0": [
          {
            "type": "input_value",
            "name": "numbercv"
          }
        ],
        "output": null,
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
      }
    );
  }
};
Blockly.Python['carbitv2_stringtonumber'] = function(block) {
  var value_numbercv = Blockly.Python.valueToCode(block, 'numbercv', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'int('+value_numbercv+')';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['carbitv2_ble_start'] = {
  init: function() {
    this.jsonInit(
      {"colour": "#cb2026", 
      "nextStatement": null, 
      "tooltip": Blockly.Msg.YOLOBIT_BLE_START_TOOLTIP, 
      "message0": Blockly.Msg.YOLOBIT_BLE_START_MESSAGE0, 
      "previousStatement": null, 
      "args0": [
        {
          "type": "input_value",
          "name": "NAME",
          "check": "String"
        }],
      "inputsInline": true,
      "helpUrl": Blockly.Msg.YOLOBIT_BLE_START_HELPURL});
  }
};

Blockly.Blocks['carbitv2_ble_on_receive_message'] = {
  init: function() {
    this.jsonInit({
      "colour": "#cb2026", 
      "nextStatement": null, 
      "tooltip": Blockly.Msg.YOLOBIT_BLE_ON_RECEIVE_MESSAGE_TOOLTIP, 
      "message0": Blockly.Msg.YOLOBIT_BLE_ON_RECEIVE_MESSAGE_MESSAGE0, 
      "previousStatement": null, 
      "args0": [
        {"variable": Blockly.Msg.YOLOBIT_BLE_ON_RECEIVE_MESSAGE_MESSAGE1, "type": "field_variable", "name": "message"}, 
        {"type": "input_dummy"}, 
        {"type": "input_statement", "name": "ACTION"}
      ],
      "helpUrl": Blockly.Msg.YOLOBIT_BLE_ON_RECEIVE_MESSAGE_HELPURL
    });
  }
};

// Any imports need to be reserved words
Blockly.Python.addReservedWords('ble_start');
Blockly.Python.addReservedWords('ble_on_rx');

Blockly.Python['carbitv2_ble_start'] = function(block) {
  Blockly.Python.definitions_['import_ble_peripheral'] = 'from carbitv2_ble_uart_peripheral import *';
  var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'ble_start(' + value_name + ')\n';
  return code;
};

Blockly.Python['carbitv2_ble_on_receive_message'] = function(block) {
  Blockly.Python.definitions_['import_ble_peripheral'] = 'from carbitv2_ble_uart_peripheral import *';
  var variable_message = Blockly.Python.variableDB_.getName(block.getFieldValue('message'), Blockly.Variables.NAME_TYPE);
  var statements_action = Blockly.Python.statementToCode(block, 'ACTION');
  // TODO: Assemble Python into code variable.
  var cbFunctionName = Blockly.Python.provideFunction_(
    'ble_on_rx_callback',
    ['def ' + Blockly.Python.FUNCTION_NAME_PLACEHOLDER_ + '(' + variable_message + '):',
      statements_action || Blockly.Python.PASS
    ]);

  var code = 'ble_on_rx(' + cbFunctionName + ')\n';
  return code;
};


Blockly.Blocks['carbitv2_gamepad_message'] = {
  init: function() {
    this.jsonInit({
  "type": "carbitv2_gamepad_message",
  "message0": "%1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "type",
      "options": [
        [
          {
            src: "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-up.svg",
            width: 15,
            height: 15,
            alt: "Lên",
          },
          "!B516"
        ],
        [
          {
            src: "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-down.svg",
            width: 15,
            height: 15,
            alt: "Xuống",
          },
          "!B615"
        ],
        [
          {
            src: "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-left.svg",
            width: 15,
            height: 15,
            alt: "Trái",
          },
          "!B714"
        ],
        [
          {
            src: "https://ohstem-public.s3.ap-southeast-1.amazonaws.com/extensions/AITT-VN/yolobit_carbit_v2/images/arrow-right.svg",
            width: 15,
            height: 15,
            alt: "Phải",
          },
          "!B814"
        ],
        [
          "A",
          "!B11:"
        ],
        [
          "B",
          "!B219"
        ],
        [
          "C",
          "!B318"
        ],
        [
          "D",
          "!B417"
        ]
      ]
    }
  ],
  "output": null,
  "colour": "#cb2026",
  "tooltip": "",
  "helpUrl": ""
}
    );
  }
};

Blockly.Python['carbitv2_gamepad_message'] = function(block) {
  // TODO: Assemble Python into code variable.
  var dropdown_type = block.getFieldValue('type');
  var code = "'" + dropdown_type + "'";
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};
