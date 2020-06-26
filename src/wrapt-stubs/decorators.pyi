#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:47:20 2020

@author: Scott Tuttle
"""

from typing import Any, Callable, Optional

def decorator(wrapper: Optional[Callable[..., Any]] = None,
              enabled: Any = None,
              adapter: Any = None) -> Callable[..., Any]: ...
