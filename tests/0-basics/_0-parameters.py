import numpy as np
import spira.all as spira


class TestDefault(spira.Cell):

    _integer = spira.IntegerField(doc='Integer docstring.')
    _float = spira.FloatField(doc='Float docstring.')
    _string = spira.StringField(doc='String docstring.')
    _bool = spira.BoolField(doc='Boolean docstring.')
    _list = spira.ListField(doc='List docstring.')
    _dict = spira.DictField(doc='Dictionary docstring.')
    _numpy = spira.NumpyArrayField(doc='Numpy Array docstring.')


class TestDefaultSet(spira.Cell):

    _integer = spira.IntegerField(default=1)
    _float = spira.FloatField(default=1.0)
    _string = spira.StringField(default='Yes')
    _bool = spira.BoolField(default=True)
    _list = spira.ListField(default=[1, 0, 3])
    _dict = spira.DictField(default={'number': 1, 'datatype': 0})
    _numpy = spira.NumpyArrayField(default=np.array([1, 2, 3]))


class TestErrors(spira.Cell):

    _integer = spira.IntegerField(default=1.0)
    _float = spira.FloatField(default=1)
    _string = spira.StringField(default=2)
    _bool = spira.BoolField(default='True')
    _list = spira.ListField(default=np.array([1, 0, 3]))
    _dict = spira.DictField(default=1)
    _numpy = spira.NumpyArrayField(default=[1, 2, 3])


class TestFields(spira.Cell):

    layer = spira.LayerField(doc='Layer docstring.')
    color = spira.ColorField(doc='Color docstring.')
    shape = spira.ShapeField(doc='Shape docstring.')
    cell = spira.CellField(doc='Cell docstring.')
    ps_layer = spira.PhysicalLayerField(doc='Player docstring.')
    # label = spira.LabelField(doc='Label docsring.')
    # port = spira.PortField(doc='Port docstring.')
    # polygon = spira.PolygonField(doc='Polygon docstring.')
    print(layer.__doc__)


if __name__ == '__main__':

    # --------------------------------------------

    cell = TestFields()

    print(TestFields.__doc__)
    
    print(TestFields.layer.__doc__)
    print(TestFields.color.__doc__)
    print(TestFields.shape.__doc__)
    print(TestFields.cell.__doc__)
    print(TestFields.ps_layer.__doc__)
    # print(TestFields.label.__doc__)
    # print(TestFields.port.__doc__)
    # print(TestFields.polygon.__doc__)

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




