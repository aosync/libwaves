# libwaves

Python library to manipulate linear combinations of harmonic oscillators


## Example

```py
n = 3
omega = 8/60*2*np.pi

nU1 = 200*1000
nU2 = 150*1000
nU3 = 20*1000
nU4 = 2*1000

# Define input signal
Fx = -nU1*(Cos(n*omega) + Sin(n*omega)) - nU2*(Cos(2*n*omega) + Sin(2*n*omega)) - nU3*(Cos(3*n*omega) + Sin(3*n*omega)) - nU4*(Cos(4*n*omega) + Sin(4*n*omega))

# Low pass filter with cutoff 1 Hz
H = lambda w: 1.0 if np.abs(w) < 1*2*np.pi else 0.0

# Calculate output signal by multiplicating each oscillator coefficient
# with corresponding return value of function
Xx = Fx.convofrf(H)

t = np.linspace(0, 10, 1000)
plt.plot(t, Xx(t))
plt.show()
```