import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

class Signal:
	def __init__(self, oscillators = {}):
		self.oscillators = oscillators
		
		badkeys = []
		for key, val in self.oscillators.items():
			if np.abs(val) == 0.0:
				badkeys.append(key)
		
		for key in badkeys:
			del self.oscillators[key]
	
	def __call__(self, t):
		r = np.complex128(0.0)
		
		for oscillator in self.oscillators.items():
			v = oscillator[1] * np.exp(1.0j*oscillator[0]*t)
		
			r += v
		
		return r
		
	def __add__(self, rhs):
		oscillators = {}
	
		for oscillator in rhs.oscillators.items():
			if not oscillator[0] in oscillators:
				oscillators[oscillator[0]] = np.complex128(0.0)
				
			oscillators[oscillator[0]] += np.complex128(oscillator[1])
		
		for oscillator in self.oscillators.items():
			if not oscillator[0] in oscillators:
				oscillators[oscillator[0]] = np.complex128(0.0)
				
			oscillators[oscillator[0]] += np.complex128(oscillator[1])
		
		return Signal(oscillators)
		
		
	def __radd__(self, lhs):
		return self + lhs
	
	def __neg__(self):
		return self * (-1)
		
	def __sub__(self, rhs):
		return self + (-rhs)
	
	def __mul__(self, rhs):
		if not issubclass(type(rhs), Signal):
			rhs = Signal({0: np.complex128(rhs)})
	
		oscillators = {}
		for lfreq in self.oscillators.keys():
			for rfreq in rhs.oscillators.keys():
				nfreq = lfreq + rfreq
				
				if not nfreq in oscillators:
					oscillators[nfreq] = np.complex128(0)
				
				oscillators[nfreq] += self.oscillators[lfreq] * rhs.oscillators[rfreq]
		
		return Signal(oscillators)
	
	def __rmul__(self, scalar):
		return self * scalar
	
	def __truediv__(self, scalar):
		return self * (1/scalar)
	
	# Get a tuple of frequencies and their associated Fourier coefficient
	def freqs(self):
		return np.array(list(self.oscillators.keys())), np.array(list(self.oscillators.values()))
	
	# Get a tuple of frequencies and their associated Fourier coefficient
	# but fold back the negative frequencies over the positive frequencies
	def realfreqs(self):
		foldback = {}
		
		for freq, val in self.oscillators.items():
			if freq < 0.0:
				continue
		
			if not freq in foldback:
				foldback[freq] = np.complex128(0)
				
			foldback[freq] += 2 * val
		
		return np.array(list(foldback.keys())), np.array(list(foldback.values()))
	
	# Calculate the power spectrum over the entire spectrum
	def power(self):
		f, Fxx = self.freqs()
		return f, np.abs(Fxx)**2
	
	# Calculate the power spectrum by folding back negative frequencies to positive
	# frequencies. Useful if the signal is real
	def realpower(self):
		f, Fxx = self.realfreqs()
		return f, np.abs(Fxx)**2 / 2
	
	# Multiply Fourier coefficient at freq w with value of function
	# evaluated at w. Typically, if frf is a frequency response function,
	# this allows for evaluating the response
	def convofrf(self, frf):
		oscillators = {}
		
		for freq, val in self.oscillators.items():
			oscillators[freq] = val * frf(freq)
		
		return Signal(oscillators)
	
class Exp(Signal):
	def __init__(self, freq):
		super().__init__({np.float128(freq): 1.0})

def Sin(freq):
	a = Exp(freq)
	b = Exp(-freq)
	
	return (a - b) / (2.0j)

def Cos(freq):
	a = Exp(freq)
	b = Exp(-freq)
	
	return (a + b) / (2.0)