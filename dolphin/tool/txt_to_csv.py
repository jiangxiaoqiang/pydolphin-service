# -*- coding: UTF-8 -*-

import pandas as pd  
  
txt = pd.read_fwf('/Users/dolphin/words_merged.txt')  
txt.to_csv('file.csv') 