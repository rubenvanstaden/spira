import numpy as np
import spira.all as spira


class TestDefault(spira.Cell):

    _integer = spira.IntegerParameter(doc='Integer docstring.')
    _float = spira.FloatParameter(doc='Float docstring.')
    _string = spira.StringParameter(doc='String docstring.')
    _bool = spira.BoolParameter(doc='Boolean docstring.')
    _list = spira.ListParameter(doc='List docstring.')
    _dict = spira.DictParameter(doc='Dictionary docstring.')
    _numpy = spira.NumpyArrayParameter(doc='Numpy Array docstring.')


class TestDefaultSet(spira.Cell):

    _integer = spira.IntegerParameter(default=1)
    _float = spira.FloatParameter(default=1.0)
    _string = spira.StringParameter(default='Yes')
    _bool = spira.BoolParameter(default=True)
    _list = spira.ListParameter(default=[1, 0, 3])
    _dict = spira.DictParameter(default={'number': 1, 'datatype': 0})
    _numpy = spira.NumpyArrayParameter(default=np.array([1, 2, 3]))


class TestErrors(spira.Cell):

    _integer = spira.IntegerParameter(default=1.0)
    _float = spira.FloatParameter(default=1)
    _string = spira.StringParameter(default=2)
    _bool = spira.BoolParameter(default='True')
    _list = spira.ListParameter(default=np.array([1, 0, 3]))
    _dict = spira.DictParameter(default=1)
    _numpy = spira.NumpyArrayParameter(default=[1, 2, 3])


class TestParameters(spira.Cell):

    layer = spira.LayerParameter(doc='Layer docstring.')
    color = spira.ColorParameter(doc='Color docstring.')
    shape = spira.ShapeParameter(doc='Shape docstring.')
    cell = spira.CellParameter(doc='Cell docstring.')
    # ps_layer = spira.PhysicalLayerParameter(doc='Player docstring.')
    # label = spira.LabelParameter(doc='Label docsring.')
    # port = spira.PortParameter(doc='Port docstring.')
    # polygon = spira.PolygonParameter(doc='Polygon docstring.')
    print(layer.__doc__)


if __name__ == '__main__':

    # --------------------------------------------

    cell = TestParameters()

    print(TestParameters.__doc__)
    
    print(TestParameters.layer.__doc__)
    print(TestParameters.color.__doc__)
    print(TestParameters.shape.__doc__)
    print(TestParameters.cell.__doc__)
    # print(TestParameters.ps_layer.__doc__)
    # print(TestParameters.label.__doc__)
    # print(TestParameters.port.__doc__)
    # print(TestParameters.polygon.__doc__)

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




