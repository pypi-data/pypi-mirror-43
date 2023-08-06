# check-device-code
校验手机设备码

## 介绍
本库用于校验手机IMEI设备码的最后一位是否正确，如没有最后一位则自动补齐。

## 使用方法
```python
import check_device_code as cdc

# 输入imei = 14位
print(cdc.check_device_doce('imei',str(86379103507858)))
# 校验失败，自动补齐
{'check': False, 'imei': '863791035078583'}

# 输入imei < 14位
print(cdc.check_device_code('imei',str(8637910350785)))
# 输入imei > 15位
print(cdc.check_device_code('imei',str(8637910350785836)))
# 输入imei != 全数字
print(cdc.check_device_code('imei',str('A63791035078583')))
# 校验失败，返回None
{'check': False, 'imei': None}

# 输入错误的imei
print(cdc.check_device_code('imei',str(863791035078587)))
# 校验失败，返回正确值
{'check': False, 'imei': '863791035078583'}

# 输入正确的imei
print(cdc.check_device_code('imei',str(863791035078583)))
# 校验成功，返回原值
{'check': True, 'imei': '863791035078583'}


```