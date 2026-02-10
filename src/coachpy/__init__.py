from typing import Any, Dict, List
import matplotlib.pyplot as plt

__version__ = "0.1.0"


class Simulation:
    """
    Een simulatie houdt variabelen bij over tijd.

    Leerlingen kunnen meerdere simulaties naast elkaar runnen om
    verschillende scenario's te vergelijken (bijv. verschillende veerconstantes).

    Example:
        >>> sim = Simulation(name="Vrije val")
        >>> t, dt = 0, 0.01
        >>> x, v, a = 10, 0, -9.81
        >>>
        >>> while t < 2:
        ...     v += a * dt
        ...     x += v * dt
        ...     t += dt
        ...     sim.track(t=t, x=x, v=v)
        >>>
        >>> sim.plot('x', against='t', ylabel='hoogte (m)')
    """

    def __init__(self, name: str = "Simulatie"):
        self.name = name
        self._history: Dict[str, List[float]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def track(self, **variables):
        """
        Sla de huidige waarden van variabelen op.

        Args:
            **variables: Naam-waarde paren van variabelen om te tracken

        Example:
            >>> sim.track(tijd=t, positie=x, snelheid=v)
        """
        for name, value in variables.items():
            if name not in self._history:
                self._history[name] = []
            self._history[name].append(float(value))

    def set_metadata(self, variable: str, unit: str = "", label: str = ""):
        """
        Voeg metadata toe aan een variabele voor mooiere plots.

        Args:
            variable: Naam van de variabele
            unit: Eenheid (bijv. "m", "m/s", "N")
            label: Menselijk leesbare naam (bijv. "Hoogte")

        Example:
            >>> sim.set_metadata('x', unit='m', label='Hoogte')
            >>> sim.set_metadata('v', unit='m/s', label='Snelheid')
        """
        if variable not in self._metadata:
            self._metadata[variable] = {}
        if unit:
            self._metadata[variable]["unit"] = unit
        if label:
            self._metadata[variable]["label"] = label

    def _get_label(self, variable: str) -> str:
        """Genereer een mooi label voor een variabele."""
        if variable not in self._metadata:
            return variable

        meta = self._metadata[variable]
        label = meta.get("label", variable)
        unit = meta.get("unit", "")

        if unit:
            return f"{label} ({unit})"
        return label

    def plot(
        self,
        *variables: str,
        against: str = None,
        title: str = None,
        xlabel: str = None,
        ylabel: str = None,
        grid: bool = True,
        figsize: tuple = (10, 6),
        style: str = "-",
        **plot_kwargs,
    ):
        """
        Maak een plot van één of meerdere variabelen.

        Args:
            *variables: Variabelen om te plotten
            against: X-as variabele (standaard: eerste variabele in track())
            title: Titel van de plot
            xlabel: Label voor x-as (automatisch gegenereerd als niet opgegeven)
            ylabel: Label voor y-as (automatisch gegenereerd als niet opgegeven)
            grid: Toon rasterlijnen
            figsize: Grootte van de figuur (breedte, hoogte)
            style: Plot stijl ('-', '--', '.-', 'o', etc.)
            **plot_kwargs: Extra argumenten voor matplotlib (color, linewidth, etc.)

        Example:
            >>> sim.plot('x', 'v', against='t', title='Vrije val')
        """
        if not self._history:
            raise ValueError("Geen data om te plotten. Gebruik eerst sim.track()")

        # Bepaal x-as
        if against is None:
            # Gebruik eerste variabele die getracked is
            against = list(self._history.keys())[0]

        if against not in self._history:
            raise ValueError(f"Variabele '{against}' niet gevonden in data")

        # Maak figuur
        plt.figure(figsize=figsize)

        # Plot elke variabele
        for var in variables:
            if var not in self._history:
                raise ValueError(f"Variabele '{var}' niet gevonden in data")

            label = self._get_label(var)
            plt.plot(
                self._history[against],
                self._history[var],
                style,
                label=label,
                **plot_kwargs,
            )

        # Labels en titel
        plt.xlabel(xlabel or self._get_label(against))

        if ylabel:
            plt.ylabel(ylabel)
        elif len(variables) == 1:
            plt.ylabel(self._get_label(variables[0]))

        plt.title(title or self.name)

        if len(variables) > 1:
            plt.legend()

        if grid:
            plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def get_data(self, variable: str) -> List[float]:
        """
        Krijg de ruwe data van een variabele.

        Dit is handig voor gevorderde leerlingen die zelf iets met de data
        willen doen (bijv. exporteren, custom plots maken, etc.)

        Args:
            variable: Naam van de variabele

        Returns:
            Lijst met alle getrackte waarden

        Example:
            >>> tijden = sim.get_data('t')
            >>> hoogtes = sim.get_data('x')
        """
        if variable not in self._history:
            raise ValueError(f"Variabele '{variable}' niet gevonden")
        return self._history[variable].copy()

    def reset(self):
        """
        Wis alle getrackte data (maar behoud metadata).

        Handig om een simulatie opnieuw te runnen zonder een nieuwe
        Simulation aan te maken.
        """
        self._history.clear()

    def __repr__(self):
        n_vars = len(self._history)
        n_points = len(next(iter(self._history.values()))) if self._history else 0
        return f"Simulation('{self.name}', {n_vars} variabelen, {n_points} datapunten)"


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


__all__ = [
    "Simulation",
    "track",
    "plot",
    "set_metadata",
    "reset",
]
