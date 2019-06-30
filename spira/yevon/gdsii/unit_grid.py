from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import Parameter
from spira.core.parameters.variables import NumberParameter
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['UnitGridContainer']


class UnitGridContainer(ParameterInitializer):
    """  """

    grids_per_unit = Parameter(fdef_name='create_grids_per_unit')
    units_per_grid = Parameter(fdef_name='create_units_per_grid')
    unit = NumberParameter(default=RDD.GDSII.UNIT)
    grid = NumberParameter(default=RDD.GDSII.GRID)

    def create_grids_per_unit(self):
        return self.unit / self.grid

    def create_units_per_grid(self):
        return self.grid / self.unit

    def validate_parameters(self):
        if self.grid > self.unit:
            raise ValueError('The grid should be smaller than the unit.')
        return True




