# PyHachi


## Quick Start

```python
from pyhachi import HachiModel
from pyhachi import BlacklistPlugin, PatternPlugin


plug_1 = BlacklistPlugin(words_list=["1989", "天安门"])
plug_2 = PatternPlugin()

model = HachiModel(plugins=[plug_1, plug_2])

query = ("1989年的夏天，我们一起在天安门广场跳舞，你还记得吗。当时的天安门有好多人。\
         我的手机号是13126658707, 我的个人网站www.zaih.com, 我的微信号xiaoxiongmao4223, QQ 472146772\
         123o4usdjfk@gmail.com, or sfjjsaf@163.com")

res = model.check(query)

print(res)

#{
#    'blacklist_qj10eo': 
#        {
#            'nigger_char': {'天安门': 2, '1989': 1},
#            'nigger_word': {'天安门': 1, '1989': 1}
#        }
#    'pattern_t9rurf':
#        {
#            'special_pattern':
#                {
#                    'wechat': ['xiaoxiongmao4223'],
#                    'telephone': ['13126658707'],
#                    'email': ['123o4usdjfk@gmail.com', 'sfjjsaf@163.com'],
#                    'QQ': ['472146772'],
#                    'url': ['www.zaih.com,']
#                }
#        }
#}
```
