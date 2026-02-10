from .simulation import Simulation

_global_sim = Simulation("Simulatie")


def track(**variables):
    """
    Shortcut: track variabelen in de globale simulatie.

    Voor simpele opdrachten hoef je niet expliciet een Simulation aan te maken.

    Example:
        >>> from coachpy import track, plot
        >>> t, x, v = 0, 10, 0
        >>> while t < 2:
        ...     v += -9.81 * 0.01
        ...     x += v * 0.01
        ...     t += 0.01
        ...     track(t=t, x=x, v=v)
        >>> plot('x', against='t')
    """
    _global_sim.track(**variables)


def plot(*variables, **kwargs):
    """Shortcut: plot vanuit de globale simulatie."""
    _global_sim.plot(*variables, **kwargs)


def set_metadata(variable: str, unit: str = "", label: str = ""):
    """Shortcut: metadata voor globale simulatie."""
    _global_sim.set_metadata(variable, unit, label)


def reset():
    """Shortcut: reset de globale simulatie."""
    _global_sim.reset()


def reset():
    _global_sim.reset()
