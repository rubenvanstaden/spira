from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import DataField
from spira.core.parameters.variables import NumberField
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['UnitGridContainer']


class UnitGridContainer(FieldInitializer):
    """  """

    grids_per_unit = DataField(fdef_name='create_grids_per_unit')
    units_per_grid = DataField(fdef_name='create_units_per_grid')
    unit = NumberField(default=RDD.GDSII.UNIT)
    grid = NumberField(default=RDD.GDSII.GRID)

    def create_grids_per_unit(self):
        return self.unit / self.grid

    def create_units_per_grid(self):
        return self.grid / self.unit

    def validate_parameters(self):
        if self.grid > self.unit:
            raise ValueError('The grid should be smaller than the unit.')
        return True




