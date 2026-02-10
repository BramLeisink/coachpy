from typing import Any, Dict, List
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, name: str = "Simulatie"):
        self.name = name
        self._history: Dict[str, List[float]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def track(self, **variables):
        for name, value in variables.items():
            if name not in self._history:
                self._history[name] = []
            self._history[name].append(float(value))

    def set_metadata(self, variable: str, unit: str = "", label: str = ""):
        if variable not in self._metadata:
            self._metadata[variable] = {}
        if unit:
            self._metadata[variable]["unit"] = unit
        if label:
            self._metadata[variable]["label"] = label

    def _get_label(self, variable: str) -> str:
        if variable not in self._metadata:
            return variable
        meta = self._metadata[variable]
        label = meta.get("label", variable)
        unit = meta.get("unit", "")
        return f"{label} ({unit})" if unit else label

    def plot(self, *variables: str, against: str = None, **kwargs):
        if not self._history:
            raise ValueError("Geen data om te plotten. Gebruik eerst sim.track()")

        against = against or list(self._history.keys())[0]
        plt.figure(figsize=kwargs.get("figsize", (10, 6)))

        for var in variables:
            plt.plot(
                self._history[against], self._history[var], label=self._get_label(var)
            )

        plt.xlabel(self._get_label(against))
        plt.title(self.name)
        if len(variables) > 1:
            plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def get_data(self, variable: str) -> List[float]:
        return self._history[variable].copy()

    def reset(self):
        self._history.clear()
