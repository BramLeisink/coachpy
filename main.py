from coachpy import *

# Initialiseer de simulatie
sim = Simulation("Vrije val met CoachPy")

# Metadata instellen (labels en eenheden)
sim.set_metadata("t", unit="s", label="Tijd")
sim.set_metadata("y", unit="m", label="Hoogte")
sim.set_metadata("v", unit="m/s", label="Snelheid")

# Beginwaarden en parameters
t = 0
dt = 0.01

y = 1.8
v = 5
g = 9.81

# Numerieke integratie (Euler-methode)
while y > 0:
    a = -g
    v = v + a * dt
    y = y + v * dt
    t += dt

    # Sla de gegevens op
    sim.track(t=t, y=y, v=v)

# Plot direct het resultaat
sim.plot("y", against="t")
