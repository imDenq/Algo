def parse_clause(clause_str):
    literals = []
    tokens = clause_str.replace('(', '').replace(')', '').replace('∨', ' ').split()
    for token in tokens:
        if token.startswith('¬'):
            literals.append((token[1:], False))
        else:
            literals.append((token, True))
    return literals

def evaluate_clause(clause, assignment):
    for var, is_positive in clause:
        if var in assignment:
            value = assignment[var]
            if (is_positive and value) or (not is_positive and not value):
                return True
    return False

def verify_sat(clauses, assignment):
    for clause in clauses:
        if not evaluate_clause(clause, assignment):
            return False
    return True

def solve_sat_backtrack(clauses, variables, assignment=None, var_index=0):
    if assignment is None:
        assignment = {}
    
    if var_index == len(variables):
        return verify_sat(clauses, assignment)
    
    var = variables[var_index]
    
    for value in [True, False]:
        assignment[var] = value
        if solve_sat_backtrack(clauses, variables, assignment, var_index + 1):
            return True
    
    del assignment[var]
    return False