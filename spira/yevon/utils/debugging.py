

__all__ = ['debug_view']


def debug_view(cell):
    D = cell.flat_expand_transform_copy()
    print('\n---------------------------------')
    print('[*] List of Ports:')
    print(D.ports)
    print('---------------------------------\n')
    D.output()

