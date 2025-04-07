from plot_kind import PlotKind
from rhs_iterator import iterate_over_rhs
from plot_kind_plotter import plot

class VM(PlotKind):
    def __init__(self):
        super().__init__()
        # Estos tres atributos en el futuro podrían no existir, xq podría haber un método que haga iterate and plot
        self.current_rhs_value = None,
        self.rhs_values = None,
        self.dual_values = None


    # Obtener la componente 'y' a registrar.
    def get_y(self, constraint_nameY):
        return constraint_nameY.dual_value

    def get_text_for_plot(self, constraint_nameX, xunit, yunit):
        xlabel='{0} {1}'.format(constraint_nameX, xunit)
        ylabel='Valor Marginal \n {0} \n{1}'.format(constraint_nameX, yunit)
        title='Valor Marginal {}'.format(constraint_nameX)
        
        return {"xlabel": xlabel, "ylabel": ylabel, "title": title}

    # AUX: En construcción. También debería ser abstracto en superclase, viendo firmas y atributos (self).
    def iterate(self, constraint_nameX, mdl, products, produccion_vars):
        constraint_nameY = mdl.get_constraint_by_name(constraint_nameX)

        self.current_rhs_value, self.rhs_values, self.dual_values = iterate_over_rhs(constraint_nameX, constraint_nameY, mdl, products, produccion_vars, self.get_y)        
        
        return self.current_rhs_value, self.rhs_values, self.dual_values
    
    def plot(self, constraint_nameX, x_unit, y_unit):
        plot_text = self.get_text_for_plot(constraint_nameX, x_unit, y_unit)
        plot(self.rhs_values, self.dual_values, self.current_rhs_value, plot_text)
        

# Comentarios de debug, entre iterate y plot
# print("rhs_values:",rhs_values)
# print("current_rhs_value:",current_rhs_value) # es el actual, el bi
# print("dual_values:", dual_values)
# print("")
# print("constraint_nameX:", constraint_nameX)
# print("constraint_nameY:", constraint_nameY)
# print("")
# print("mdl:", mdl)
# print("mdl:", mdl.solution)
# # if 0 not in rhs_values, significa que antes de su mín es incompatible