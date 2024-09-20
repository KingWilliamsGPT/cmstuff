from cmstuff import get_caller_module, CallerStack, get_logger

lg = get_logger(outputs=('console', 'rotatefile'))


def test():
    print('dept 1..')

    print('ME', get_caller_module(_stack=CallerStack.ME))
    print('BASE', get_caller_module(_stack=CallerStack.BASE))
    print('MY_CALLER', get_caller_module(_stack=CallerStack.MY_CALLER))
    

if __name__ == '__main__':
    # test()

    lg.debug('this is a debug')
    lg.warning('this is a warning')
    lg.error('this is an error')
    lg.critical('this is a critical')
