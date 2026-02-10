# CoachPy

**Een modern, Python-gebaseerd alternatief voor Coach7.**

CoachPy is een Python-package ontworpen voor natuurkundig modelleren in het voortgezet onderwijs. Waar programma's zoals Coach7 gebruikmaken van een gesloten omgeving en de verouderde 'CoachTaal' (gebaseerd op Pascal), biedt CoachPy leerlingen de kans om te werken met een wereldstandaard: **Python**.

## Waarom CoachPy?

In plaats van een specifieke tool te leren bedienen, leren leerlingen met CoachPy een algemene academische vaardigheid.

- **Overdraagbaar:** De concepten (variabelen, loops, functies) zijn direct toepasbaar bij informatica, wiskunde en vervolgstudies.
- **Geen Plafond:** CoachPy dient als 'steiger'. Het verlaagt de instap met handige functies voor metadata en plotting, maar zit diepergaand onderzoek niet in de weg.
- **Modern Ecosystem:** Gebruik de beste editors (VS Code, Cursor, PyCharm) met volledige ondersteuning voor syntax highlighting en foutopsporing.

## Installatie

Installeer de library eenvoudig via pip:

```bash
pip install coachpy

```

## Voorbeeld: Een Vrije Val Modelleren

Met CoachPy schrijf je natuurkundige modellen die leesbaar en transparant zijn.

```python
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

```

## Visie

CoachPy is ontstaan vanuit de overtuiging dat modelleren niet gaat over het leren van een programma, maar over het leren denken in systemen. Door de overstap te maken van Coach7 naar Python, maken we natuurkunde-onderwijs toekomstbestendig en technisch relevant.