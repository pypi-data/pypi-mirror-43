#!/usr/bin/env python3
# encoding: utf-8

import random
import string

def plugin_name_generator(size=6):
    chars=string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
