## Anomaly detection algorithms.

**Requirement**

1. Compiler with c++11 support (gcc.4.9 or more)
2. Cython 0.23 or more
3. Numpy

**Install package**

Installing to the python library directory.

``python setup.py install``

**Example**
```python
import numpy as np 
import sklearn.metrics as mt 
import pyad  
#%%
# data 
N, D = 400, 5
w = np.random.randn(N, D)
w_score = w.copy()

# Train anomlay detector
# LODA
loda = pyad.Loda()
loda.train(w)
# IForest
iforest = pyad.IsolationForest()
iforest.train(w)

# Add anomalies 
w_score[:3,2:5] = np.random.randn(3, 3)*5
w_score[3:6,1:3] = np.random.randn(3, 2)*-5
label = np.zeros(N)
label[:6] = 1.0 # label as anomalies 

# score 
loda_score = loda.score(w_score)
iforest_score = iforest.score(w_score)

# Computer AUC metrics using sklearn package.
print("AUC(loda): {}, AUC(iForest): {}".format(mt.roc_auc_score(label, loda_score), 
mt.roc_auc_score(label, iforest_score)))
```

### Status
[![Build Status](https://travis-ci.com/tadeze/pyad.svg?token=4ykfwWQySq2ndZvpPqdz&branch=master)](https://travis-ci.com/tadeze/pyad)

**MIT License**


``` Copyright (c) 2017 Tadesse Zemicheal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.```
  
  
  
