# ewstools
A module to compute early warning signals (EWS) from time-series data.
Dependencies include:
  - standard python libraries: numpy, pandas, scipy, matplotlib
  - LMFIT: download [here](https://lmfit.github.io/lmfit-py/installation.html)


## ews_compute.py
File for function `ews_compute`.  
`ews_compute` takes in Series data and outputs user-specified EWS in a DataFrame.


**Input** (default value)
- *raw_series* : pandas Series indexed by time 
- *roll_window* (0.25) : size of the rolling window (as a proportion of the length of the data)
- *smooth* (True) : if True, series data is detrended with a Gaussian kernel
- *band_width* (0.2) : bandwidth of Gaussian kernel
- *ews* ( ['*var*', '*ac*', '*smax*'] ) : list of strings corresponding to the desired EWS. Options include
  - '*var*'   : Variance
  - '*ac*'    : Autocorrelation
  - '*sd*'    : Standard deviation
  - '*cv*'    : Coefficient of variation
  - '*skew*'  : Skewness
  - '*kurt*'  : Kurtosis
  - '*smax*'  : Peak in the power spectrum
  - '*cf*'    : Coherence factor
  - '*aic*'   : AIC weights
- *lag_times* ( [1] ) : list of integers corresponding to the desired lag times for AC
- *ham_length* (40) : length of the Hamming window (used to compute power spectrum)
- *ham_offset* (0.5) : offset of Hamming windows as a proportion of *ham_length*
- *w_cutoff* (1) : cutoff frequency (as a proportion of maximum frequency attainable from data)
    
**Output**
- DataFrame indexed by time with columns corresponding to each EWS



## ews_compute_run.py
An example script that runs `ews_compute` on times-series data of a stochastic simulation of May's 
harvesting model. It also shows how to compute kendall tau values and plot results. This
can be used as a template for EWS of times-series data.


## ews_compute_runMulti.py
An example script that runs `ews_compute` on multiple time-series data and outputs
EWS as a distribution over realisations.















