from typing import Any, Dict, List, Optional
import matplotlib.pyplot as plt


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
        self._history: Dict[str, List[float]] = {"step": []}
        self._metadata: Dict[str, Dict[str, Any]] = {
            "step": {"label": "Stappen", "unit": ""}
        }
        self._current_step = 0

    def track(self, **variables: float) -> None:
        """
        Sla de huidige waarden van variabelen op.

        Args:
            **variables: Naam-waarde paren van variabelen om te tracken

        Example:
            >>> sim.track(tijd=t, positie=x, snelheid=v)
        """
        self._current_step += 1
        self._history["step"].append(float(self._current_step))

        for name, value in variables.items():
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name} moet een getal zijn, niet {type(value)}")

            if name not in self._history:
                self._history[name] = [float("nan")] * (self._current_step - 1)

            self._history[name].append(float(value))

        for key in self._history:
            if key != "step" and len(self._history[key]) < self._current_step:
                self._history[key].append(float("nan"))

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
        block: bool = True,
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
            block: Indien False, opent de plot in een nieuw venster zonder het programma te pauzeren.
            **plot_kwargs: Extra argumenten voor matplotlib (color, linewidth, etc.)
        """
        if not self._history or not self._history.get("step"):
            raise ValueError("Geen data om te plotten. Gebruik eerst sim.track()")

        x_axis = against if against else "step"

        if x_axis not in self._history:
            raise ValueError(f"Variabele '{x_axis}' niet gevonden in data")

        if not variables:
            variables = [k for k in self._history.keys() if k != x_axis]

        plt.figure(figsize=figsize)

        for var in variables:
            if var not in self._history:
                raise ValueError(f"Variabele '{var}' niet gevonden in data")

            plt.plot(
                self._history[x_axis],
                self._history[var],
                style,
                label=self._get_label(var),
                **plot_kwargs,
            )

        plt.xlabel(xlabel or self._get_label(x_axis))

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

        plt.show(block=block)

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
        self._history = {"step": []}
        self._metadata = {"step": {"label": "Stappen", "unit": ""}}
        self._current_step = 0

    def __repr__(self):
        n_vars = len(self._history)
        n_points = len(next(iter(self._history.values()))) if self._history else 0
        return f"Simulation('{self.name}', {n_vars} variabelen, {n_points} datapunten)"
