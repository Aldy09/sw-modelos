# Import libs
import sys
import matplotlib.pyplot as plt
from docplex.mp.model import Model
from docplex.mp.relax_linear import LinearRelaxer

#def load_data():
from data import load_data

# Create the model with constraints and objective
def create_model():
    name, products, resources, consumptions = load_data()
    mdl = Model(name)

    produccion_vars = mdl.continuous_var_dict(products, name='produccion')

    # --- constraints ---

    # --- resources disp equipo ---
    mdl.add_constraints((mdl.sum(produccion_vars[p] * consumptions[p[0], res[0]] for p in products) <= res[1], 'Disp_%s' % res[0]) for res in resources)

    # max demand
    mdl.add_constraints((produccion_vars[p] <= p[2], 'DemandMax_%s' % p[0]) for p in products)

    # min demand
    mdl.add_constraints((produccion_vars[p] >= p[3], 'DemandMin_%s' % p[0]) for p in products)

    # --- print information ---
    mdl.print_information()

    total_benefit = mdl.sum(produccion_vars[p] * p[1] for p in products)

    # --- set the objective ---
    mdl.maximize(total_benefit)

    return mdl, produccion_vars, products

# Solve the model
def solve_model(mdl, produccion_vars, products):
    solution = mdl.solve()

    if not solution:
        print("Model cannot be solved.")
        sys.exit(1)

    obj = mdl.objective_value

    print("* Production model solved with objective: {:g}".format(obj))
    print("* Total benefit=%g" % mdl.objective_value)
    for p in products:
        print("Production of {product}: {prod_var}".format(product=p[0], prod_var=produccion_vars[p].solution_value))

######### FUNCIONES COMUNES #########

# Perform sensitivity analysis of the RHS
### Aux: VM, Funcional
def perform_sensitivity_analysis(mdl):
    lp = LinearRelaxer.make_relaxed_model(mdl)
    lp.solve()
    cpx = lp.get_engine().get_cplex()

    return cpx.solution.sensitivity.rhs()

# Adjust RHS and solve 
### Aux: misma función que VM, funcional
  # mdl, products, produccion_vars
def solve(c, rhs_value, mdl, products, produccion_vars):
    print("---")
    print("- Adjusting RHS to: {0}".format(rhs_value))
    c.rhs = rhs_value
    solution = mdl.solve()
    
    if solution is not None:       
        print("* Production model solved with objective: {:g}".format(solution.objective_value))
        print("* Total benefit=%g" % solution.objective_value)
        for p in products:
            print("Production of {product}: {prod_var}".format(product=p[0], prod_var=produccion_vars[p].solution_value))
        return solution
    else:
        print("No solution found for RHS value: {0}".format(rhs_value))
        return None  # Return None to indicate that the model is infeasible at this point


# Plot the chart: objective vs. rhs value

import matplotlib.pyplot as plt
import matplotlib


# AUX: VM
# Optional: xunit: unit to plot for x-axis
# Optional: yunit: unit to plot for y-axis
def plot(xunit, yunit, rhs_values, dual_values, real_rhs_value, constraint_nameX):

    # Set default font size for all text elements
    matplotlib.rcParams.update({'font.size': 18})
    
    # Dibujar líneas horizontales entre los puntos
    for i in range(len(rhs_values) - 1):
        plt.hlines(dual_values[i], rhs_values[i], rhs_values[i + 1], linewidth=6, color='C0')
        print("plt.hline dual_values[i], rhs_values[i], rhs_values[i + 1]:", dual_values[i], rhs_values[i], rhs_values[i + 1]) # debug
        # aux: es una línea horizontal con valor y=dual y valor x= de inicial a final.        
          
    # Set the x-axis and y-axis ticks to the values we are printing
    aux_locs, aux_labels = plt.xticks(rhs_values)
    print("[debug], returned ticks:", aux_locs)
    plt.yticks(dual_values)
    
    #Print current real value
    print("[debug] real_rhs_value:", real_rhs_value)
    plt.axvline(x=real_rhs_value, color='g', linestyle='--', label='Valor actual')

    plt.xlabel('{0} {1}'.format(constraint_nameX, xunit), labelpad=20, color='#DC143C')
    plt.ylabel('Valor Marginal \n {0} \n{1}'.format(constraint_nameX, yunit), rotation=0, labelpad=90, color='#DC143C')
    plt.title('Valor Marginal {}'.format(constraint_nameX), pad=30)
    plt.grid(True, which='both', linestyle='--', linewidth=0.2, color='gray', alpha=0.7)
    
    # Se puede ajustar la rotación y tamaño, si los números están muy cerca y se enciman
    plt.xticks(rotation=0, ha='right') # rotation=45, fontsize 18
    
    # Extender el último rango un poco hacia la derecha
    x_start = rhs_values[-1] # Punto donde comienza la línea
    x_offset = 20
    y_value = 0
    plt.hlines(y=y_value, xmin=x_start, xmax=x_start + x_offset, color='C0', linewidth=6)
    
    # Dibujar un vector con origen al final del último punto (extendido) y dirección hacia el infinito horizontalmente
    plt.annotate('', xy=(plt.xlim()[1], dual_values[-1]), xytext=(x_start + x_offset, dual_values[-1]),
             arrowprops=dict(arrowstyle="->", lw=2, color='C0', linewidth=30))
    
    plt.figure(figsize=(20, 10))
    plt.show()