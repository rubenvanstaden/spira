import spira
import numpy as np
from spira.core import param


class TestDefault(spira.Cell):

    _integer = param.IntegerField(doc='Integer docstring.')
    _float = param.FloatField(doc='Float docstring.')
    _string = param.StringField(doc='String docstring.')
    _bool = param.BoolField(doc='Boolean docstring.')
    _list = param.ListField(doc='List docstring.')
    _dict = param.DictField(doc='Dictionary docstring.')
    _numpy = param.NumpyArrayField(doc='Numpy Array docstring.')


class TestDefaultSet(spira.Cell):

    _integer = param.IntegerField(default=1)
    _float = param.FloatField(default=1.0)
    _string = param.StringField(default='Yes')
    _bool = param.BoolField(default=True)
    _list = param.ListField(default=[1, 0, 3])
    _dict = param.DictField(default={'number': 1, 'datatype': 0})
    _numpy = param.NumpyArrayField(default=np.array([1, 2, 3]))


class TestErrors(spira.Cell):

    _integer = param.IntegerField(default=1.0)
    _float = param.FloatField(default=1)
    _string = param.StringField(default=2)
    _bool = param.BoolField(default='True')
    _list = param.ListField(default=np.array([1, 0, 3]))
    _dict = param.DictField(default=1)
    _numpy = param.NumpyArrayField(default=[1, 2, 3])


class TestFields(spira.Cell):

    layer = param.LayerField(doc='Layer docstring.')
    color = param.ColorField(doc='Color docstring.')
    label = param.LabelField(doc='Label docsring.')
    port = param.PortField(doc='Port docstring.')
    shape = param.ShapeField(doc='Shape docstring.')
    cell = param.CellField(doc='Cell docstring.')
    ps_layer = param.PhysicalLayerField(doc='Player docstring.')
    polygon = param.PolygonField(doc='Polygon docstring.')
    print(layer.__doc__)


if __name__ == '__main__':

    # --------------------------------------------

    cell = TestFields()

    print(TestFields.__doc__)
    
    print(TestFields.layer.__doc__)
    print(TestFields.color.__doc__)
    print(TestFields.label.__doc__)
    print(TestFields.port.__doc__)
    print(TestFields.shape.__doc__)
    print(TestFields.cell.__doc__)
    print(TestFields.ps_layer.__doc__)
    print(TestFields.polygon.__doc__)

    # print(cell.layer.__doc__)
    # print(cell.color.__doc__)
    # print(cell.label.__doc__)
    # print(cell.port.__doc__)
    # print(cell.shape.__doc__)
    # print(cell.cell.__doc__)
    # print(cell.ps_layer.__doc__)
    # print(cell.polygon.__doc__)

    # print('Layer: {}'.format(cell.layer))
    # print('Color: {}'.format(cell.color))
    # print('Label: {}'.format(cell.label))
    # print('Port: {}'.format(cell.port))
    # print('Cell: {}'.format(cell.cell))
    # print('Shape: {}'.format(cell.shape))
    # print('PLayer: {}'.format(cell.ps_layer))
    # print('Polygon: {}'.format(cell.polygon))

    # --------------------------------------------

    # cell = TestDefault()

    # print(TestDefault._integer.__doc__)
    # print(TestDefault._float.__doc__)
    # print(TestDefault._string.__doc__)
    # print(TestDefault._bool.__doc__)
    # print(TestDefault._list.__doc__)
    # print(TestDefault._dict.__doc__)
    # print(TestDefault._numpy.__doc__)

    # print('Integer: {}'.format(cell._integer))
    # print('Float: {}'.format(cell._float))
    # print('String: {}'.format(cell._string))
    # print('Bool: {}'.format(cell._bool))
    # print('List: {}'.format(cell._list))
    # print('Dist: {}'.format(cell._dict))
    # print('Numpy: {}'.format(cell._numpy))
    
    # --------------------------------------------
    
    # cell = TestDefaultSet()
    # print('Integer: {}'.format(cell._integer))
    # print('Float: {}'.format(cell._float))
    # print('String: {}'.format(cell._string))
    # print('Bool: {}'.format(cell._bool))
    # print('List: {}'.format(cell._list))
    # print('Dist: {}'.format(cell._dict))
    # print('Numpy: {}'.format(cell._numpy))
    
    # --------------------------------------------
    
    # cell = TestErrors()
    # print('Integer: {}'.format(cell._integer))
    # print('Float: {}'.format(cell._float))
    # print('String: {}'.format(cell._string))
    # print('Bool: {}'.format(cell._bool))
    # print('List: {}'.format(cell._list))
    # print('Dist: {}'.format(cell._dict))
    # print('Numpy: {}'.format(cell._numpy))




