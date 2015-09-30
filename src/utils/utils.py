# Devuelve los factores en los que aparece una variable
def appearing_factors(variable, factors):
    return [f for f in factors if variable in f.factors]


# Ajustar la clave si se compone de un solo elemento
def proper_key(key):
    new_key = tuple(key)
    if len(new_key) == 1:
        new_key = new_key[0]
    return new_key