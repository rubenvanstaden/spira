import gdspy
import inspect

from core.initializer import ElementalInitializer


class ARef(gdspy.CellArray, ElementalInitializer):
    """

    """

    def __init__(self, structure, columns, rows, spacing, midpoint, **kwargs):
        ref_cell = structure.gdspycell

        required_params = {'rotation': None,
                           'magnification': None,
                           'reflection': False}

        s1 = set(required_params.keys())
        s2 = set(kwargs.keys())
        use_default = list(s1-s2)
        for key in use_default:
            kwargs[key] = required_params[key]

        for key, value in kwargs.items():
            setattr(self, key, value)

        gdspy.CellArray.__init__(self, ref_cell=ref_cell, 
                                 columns=columns, 
                                 rows=rows,
                                 spacing=spacing, 
                                 midpoint=midpoint, 
                                 rotation=self.rotation,
                                 magnification=self.magnification, 
                                 reflection=self.reflection)

        Reference.__init__(self, reference=structure)

    def __repr__(self):
        name = self.ref.name
        return ('[SPiRA: ARef] (\"{0}\", at ({1[0]}, {1[1]}), rotation {2}, magnification {3}, reflection {4})').format(name, self.midpoint, self.rotation, self.magnification, self.reflection)

    def __str__(self):
        return self.__repr__()

    def add_to_cell(self, cell):
        A = gdspy.CellArray(
            self.ref_cell,
            self.columns,
            self.rows,
            self.spacing,
            self.midpoint,
            self.rotation,
            self.magnification,
            self.reflection)
        cell.add(A)






