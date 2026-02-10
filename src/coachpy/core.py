from .simulation import Simulation

_global_sim = Simulation("Simulatie")


def track(**variables):
    _global_sim.track(**variables)


def plot(*variables, **kwargs):
    _global_sim.plot(*variables, **kwargs)


def set_metadata(variable: str, unit: str = "", label: str = ""):
    _global_sim.set_metadata(variable, unit, label)


def reset():
    _global_sim.reset()
