import utils.utils as utils

from inference.Factor import Factor


def project_observation(appearing_factors, evidence_var, relevant_factors, eliminated_factors, initial_factors, evidence_variables):

    factor = appearing_factors.pop(0)

    # Si no es un factor intermedio, lo ponemos en la lista de eliminados.
    if factor in initial_factors:
        eliminated_factors.append(factor)

    relevant_factors.remove(factor)

    # Si ademas el factor incluia otras variables, crear el nuevo factor resultante de realizar la observacion.
    if factor.evidence_variables():
        factors = list(factor.factors)
        factors.remove(evidence_var.observed_variable)

        # Mantener indices sucesivos.
        new_factor_is_final = len(set(factors) & set([ev.observed_variable for ev in evidence_variables])) == 0
        new_factor = Factor(factors, __generate_new_cpt(factor, evidence_var), new_factor_is_final)

        relevant_factors.append(new_factor)


def __generate_new_cpt(factor, evidence_var):
    new_cpt = {}
    evidence_var_position = factor.factors.index(evidence_var.observed_variable)

    for key in factor.cpt.keys():

        if key[evidence_var_position] == evidence_var.observed_value:
            new_key = list(key)
            new_key.pop(evidence_var_position)
            new_key = utils.proper_key(new_key)
            new_cpt[new_key] = factor.cpt.get(key)

    return new_cpt