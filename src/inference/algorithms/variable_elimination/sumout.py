import copy
import itertools
import utils.utils as utils

from inference.Factor import Factor


# Obtener las variables ocultas
def get_hidden_variables(relevant_factors, query_variable):

    hidden_vars = [copy.copy(factor.factors) for factor in relevant_factors]

    hidden_vars = set(itertools.chain.from_iterable(hidden_vars)) - set([query_variable])

    return hidden_vars


def sum_out(elimination_variable, relevant_factors, mode, eliminated_factors, query_variable):

    appearing_factors = utils.appearing_factors(elimination_variable, relevant_factors)

    if mode == 'verbose':

        print('Procesando ' + str(elimination_variable) + '...\n')
        print('Factores en los que aparece: ' + str([str(f) for f in appearing_factors]))

    __get_final_factor(appearing_factors, elimination_variable, relevant_factors, eliminated_factors, query_variable, mode)


def __get_final_factor(appearing_factors, elimination_variable, relevant_factors, eliminated_factors, query_variable, mode):

    while(len(appearing_factors) > 1):

            f1 = appearing_factors.pop(0)
            if f1 in relevant_factors:
                relevant_factors.remove(f1)
                eliminated_factors.append(f1)

            f2 = appearing_factors.pop(0)
            if f2 in relevant_factors:
                relevant_factors.remove(f2)
                eliminated_factors.append(f2)

            new_factor = multiply(f1, f2)
            appearing_factors.append(new_factor)

    # Factor final resultante de eliminar la variable en cuestion multiplicando los factores en los que aparece 2 a 2.
    resulting_factor = appearing_factors[0]

    # Si la variable aparecia en un solo factor, eliminar de factores relevantes ya que no habra sido eliminada anteriormente.
    if resulting_factor in relevant_factors:
        relevant_factors.remove(resulting_factor)

    # Si la variable no es de consulta, agrupar el factor resultante por ella.
    if elimination_variable != query_variable:
        resulting_factor = __group_factor_by(resulting_factor, elimination_variable)

    # Si hay un factor resultante (no es None) y no esta en los factores relevantes, ponerlo entre ellos.
    if resulting_factor and (resulting_factor not in relevant_factors):
        relevant_factors.append(resulting_factor)

    if mode == 'verbose':
        print('Factor resultante: ' + str(resulting_factor))
        print('\nFactores actuales: ' + str([str(factor) for factor in relevant_factors]))
        print('Factores eliminados: ' + str([str(factor) for factor in eliminated_factors]) + '\n')


def multiply(f1, f2):
    """
    Devuelve el producto de dos factores.

    @type  f1: Factor
    @param f1: Primer factor.

    @type  f2: Factor
    @param f2: Segundo factor.

    @rtype:  Factor
    @return: Factor resultante de realizar la multiplicacion.
    """
    # Obtener las variables que aparecen en ambos factores.
    f1_vars = copy.copy(f1.factors)
    f2_vars = copy.copy(f2.factors)

    # Calcular interseccion entre las variables de ambos factores.
    vars_intersection = list(set(f1_vars) & set(f2_vars))

    vars_indexes = [[], []]

    # Ver la posicion que ocupa cada variable comun a ambos factores en cada uno de ellos.
    for var in vars_intersection:
        vars_indexes[0].append(f1_vars.index(var))
        vars_indexes[1].append(f2_vars.index(var))

    reversed_indexes = copy.copy(vars_indexes[0])
    reversed_indexes.sort(reverse = True)

    f1_cpt = f1.cpt
    f2_cpt = f2.cpt

    new_cpt = {}
    for k1 in f1_cpt.keys():

        for k2 in f2_cpt.keys():

            # Obtener los valores de dominio para cada variable de la intersección en cada entrada de la tabla de probabilidad del primer factor.
            k1_domain_value = []
            if isinstance(k1, str):
                k1_domain_value = [k1]
            else:
                for var_index_f1 in vars_indexes[0]:
                    k1_domain_value.append(k1[var_index_f1])

            # Obtener los valores de dominio para cada variable de la intersección en cada entrada de la tabla de probabilidad del segundo factor.
            k2_domain_value = []
            if isinstance(k2, str):
                k2_domain_value = [k2]
            else:
                for var_index_f2 in vars_indexes[1]:
                    k2_domain_value.append(k2[var_index_f2])

            # Si coinciden los valores del dominio, multiplicar.
            if k1_domain_value == k2_domain_value:

                new_key = list(k1)

                if isinstance(k1, str):
                    new_key = []
                else:
                    for var_index_f1 in reversed_indexes:
                        new_key.pop(var_index_f1)

                if isinstance(k2, str):
                    new_key += list([k2])
                else:
                    new_key += list(k2)

                new_key = utils.proper_key(new_key)
                new_cpt[new_key] = f1_cpt[k1] * f2_cpt[k2]

    new_factors = f1_vars
    for var_index_f1 in reversed_indexes:
        new_factors.pop(var_index_f1)

    new_factors += f2_vars
    new_factor = Factor(new_factors, new_cpt, False)

    return new_factor


def __group_factor_by(factor, variable):
    """
    Agrupa el factor por la variable deseada.

    @type  factor: Factor
    @param factor: Factor a agrupar.

    @type  variable: Node
    @param variable: Variable por la que agrupar.

    @rtype:  Factor
    @return: Factor resultante de agrupar la variable.
    """
    new_factor = None

    if len(factor.factors) > 1:
        var_position = factor.factors.index(variable)

        new_cpt = {}

        keys = copy.copy(list(factor.cpt.keys()))

        while(keys):

            key = keys.pop(0)
            keys_to_be_grouped = []
            domain = set(variable.domain) - set([key[var_position]])

            # Generar todas las variantes posibles de key con el dominio de la variable por la que se agrupa.
            for domain_value in domain:
                k = list(key)
                k[var_position] = domain_value
                k = utils.proper_key(k)
                keys.remove(k)
                keys_to_be_grouped.append(k)

            # Sumar los valores de todas esas tuplas.
            summatory = factor.cpt[key]
            for key in keys_to_be_grouped:
                summatory += factor.cpt[key]

            # Actualizar nueva CPT.
            new_key = list(key)
            new_key.pop(var_position)
            new_key = utils.proper_key(new_key)
            new_cpt[new_key] = summatory

        new_factors = [f for f in factor.factors if f != variable]
        new_factor = Factor(new_factors, new_cpt)

    return new_factor