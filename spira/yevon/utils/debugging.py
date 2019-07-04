

__all__ = ['debug_view']


def debug_view(cell):
    D = cell.expand_flat_copy()
    print('\n---------------------------------')
    print('[*] List of Ports:')
    print(D.ports)
    print('---------------------------------\n')
    D.gdsii_output()

