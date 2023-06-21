from typing import Optional
import warnings


import pint


blessed_units = dict()
blessed_units["rad"] = ["deg"]
blessed_units["deg"] = ["rad"]
blessed_units["fs"] = ["ps", "ns"]
blessed_units["ps"] = ["fs", "ns"]
blessed_units["ns"] = ["fs", "ps"]
blessed_units["nm"] = ["wn", "eV", "meV", "Hz", "THz", "GHz"]
blessed_units["wn"] = ["nm", "eV", "meV", "Hz", "THz", "GHz"]
blessed_units["um"] = ["mm", "cm", "in"]
blessed_units["mm"] = ["um", "cm", "in"]
blessed_units["cm"] = ["um", "nm", "in"]
blessed_units["in"] = ["um", "nm", "cm"]
blessed_units["degC"] = ["degF", "K"]
blessed_units["degF"] = ["degC", "K"]
blessed_units["K"] = ["degC", "degF"]
blessed_units["s"] = ["min", "hour"]
blessed_units["min"] = ["s", "hour"]
blessed_units["hour"] = ["min", "hour"]


ureg = pint.UnitRegistry()
ureg.define("wavenumber = 1 / cm = cm^{-1} = wn")

delay = pint.Context("delay", defaults={"n": 1, "num_pass": 2})
delay.add_transformation(
    "[length]", "[time]", lambda ureg, x, n=1, num_pass=2: num_pass * x / ureg.speed_of_light * n
)
delay.add_transformation(
    "[time]", "[length]", lambda ureg, x, n=1, num_pass=2: x / num_pass * ureg.speed_of_light / n
)
ureg.enable_contexts("spectroscopy", delay)

def converter(val, current_unit, destination_unit):
    """Convert from one unit to another.

    Parameters
    ----------
    val : number
        Number to convert.
    current_unit : string
        Current unit.
    destination_unit : string
        Destination unit.

    Returns
    -------
    number
        Converted value.
    """
    try:
        val = ureg.Quantity(val, current_unit).to(destination_unit).magnitude
    except (pint.errors.DimensionalityError, pint.errors.UndefinedUnitError, AttributeError):
        if current_unit is not None and destination_unit is not None:
            warnings.warn(
                f"conversion {current_unit} to {destination_unit} not valid: returning input"
            )
    except ZeroDivisionError:
        warnings.warn(
            f"conversion {current_unit} to {destination_unit} resulted in ZeroDivisionError: returning inf"
        )
        return float("inf")
    return val


convert = converter


def get_valid_conversions(units, options=blessed_units) -> tuple:
    if units in options:
        return options[units]
    return tuple(i for i in options if is_valid_conversion(units, i))


def is_valid_conversion(a, b, blessed=True) -> bool:
    if a is None:
        return b is None
    if a in blessed_units:
        return b in blessed_units[a]
    if blessed and a in blessed_units and b in blessed_units:
        blessed_energy_units = {"nm", "wn", "eV", "meV", "Hz", "THz", "GHz"}
        if a in blessed_energy_units:
            return b in blessed_energy_units
        blessed_delay_units = {"fs", "ps", "ns", "mm_delay"}
        if a in blessed_delay_units:
            return b in blessed_delay_units
        return ureg.Unit(a).dimensionality == ureg.Unit(b).dimensionality
    try:
        return ureg.Unit(a).is_compatible_with(b, "spectroscopy")
    except pint.UndefinedUnitError:
        return False

