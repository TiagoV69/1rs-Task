import math

# --- Constantes del Modelo ---
# Este archivo contiene la logica de negocio y los calculos del modelo de poblacion.
# No depende de la interfaz grafica y puede ser reutilizado en otros contextos.

BASE_YEAR: int = 2023
INITIAL_POPULATION_MILLIONS: float = 2.5
ANNUAL_GROWTH_RATE: float = 0.03


def compute_population_for_year(year: int) -> int:
    """Devuelve la población estimada (personas) para un año >= BASE_YEAR.

    Modelo: P(year) = P0 * (1 + r)^(year - BASE_YEAR)
    Donde P0 está en personas.
    """
    if year < BASE_YEAR:
        raise ValueError(f"El año debe ser mayor o igual a {BASE_YEAR}.")
    years_elapsed: int = year - BASE_YEAR
    p0_people: float = INITIAL_POPULATION_MILLIONS * 1_000_000.0
    population: float = p0_people * ((1.0 + ANNUAL_GROWTH_RATE) ** years_elapsed)
    return int(round(population))


def compute_year_to_reach_population(
    target_millions: float,
    strictly_greater: bool = False,
) -> int:
    """Devuelve el año en el que se alcanza (>=) o se supera (>) la población objetivo.

    - target_millions: población objetivo en millones de personas
    - strictly_greater: si True, devuelve el primer año en que P > objetivo;
                        si False, el primer año en que P >= objetivo.
    """
    if target_millions <= 0:
        raise ValueError("La población objetivo debe ser positiva.")

    p0_people: float = INITIAL_POPULATION_MILLIONS * 1_000_000.0
    target_people: float = target_millions * 1_000_000.0

    # Caso trivial: ya estamos en/por encima del objetivo (según modalidad)
    if p0_people >= target_people:
        return BASE_YEAR

    # Cálculo base usando logaritmos
    growth_factor: float = 1.0 + ANNUAL_GROWTH_RATE
    # n_inclusive es el mínimo n entero con P0 * growth_factor^n >= target
    n_inclusive: int = max(
        0,
        int(math.ceil(math.log(target_people / p0_people, growth_factor))),
    )

    # ajuste si se requiere superar estrictamente y justo se iguala
    if strictly_greater:
        # Si con 'n_inclusive' se queda igual o por debajo, avanzamos hasta que sea > (mayorr)
        while True:
            pn: float = p0_people * (growth_factor ** n_inclusive)
            if pn > target_people:
                break
            n_inclusive += 1

    year: int = BASE_YEAR + n_inclusive
    return year


def format_people_to_millions(value_people: int) -> str:

    millions: float = value_people / 1_000_000.0
    return f"{millions:,.3f} millones".replace(",", "_").replace(".", ",").replace("_", ".")