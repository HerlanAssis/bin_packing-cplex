# coding: utf-8
import sys
from docplex.cp.model import CpoModel

'''
No problema de bin packing (ou problema do empacotamento),
objetos de diferentes volumes devem ser embalados em um número
finito de bandejas ou recipientes de volume V de uma forma que
minimize o número de recipientes utilizados.

https://pt.wikipedia.org/wiki/Problema_do_empacotamento
'''


def bin_packing_cplex(mdl, n, c, w_j):
    # -----------------------------------------------------------------------------
    # Inicializando dados
    # -----------------------------------------------------------------------------
    items = range(n)
    bins = range(n)

    y = [mdl.integer_var(min=0, max=1, name="y{}:".format(bin))
         for bin in bins]

    x = [[mdl.integer_var(min=0, max=1, name="X:{}-{}".format(bin, item))
          for item in items] for bin in bins]
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Construindo o modelo
    # -----------------------------------------------------------------------------

    # função objetivo
    fo = mdl.sum(y[bin] for bin in bins)
    mdl.add(mdl.minimize(fo))

    # sujeito a
    mdl.add(mdl.sum([w_j[item]*x[bin][item]
                     for item in items]) <= c*y[bin] for bin in bins)
    mdl.add(mdl.sum([x[bin][item] for bin in bins]) == 1 for item in items)
    # -----------------------------------------------------------------------------


if __name__ == "__main__":
    n = 10  # number os items
    c = 10  # volume of the bin
    w_j = [7, 9, 2, 8, 4, 6, 7, 8, 3, 6]

    mdl = CpoModel()
    bin_packing_cplex(mdl, n, c, w_j)

    print("\nImprimindo solução....")
    msol = mdl.solve(TimeLimit=60, Workers=1)

    if msol:
        print(msol.print_solution())
        print("Status: " + msol.get_solve_status())
    else:
        print("Nenhuma solução encontrada")
