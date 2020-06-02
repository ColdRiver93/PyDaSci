import main_pds


def entry_point(argv):
    print(argv)
    main_pds.begin(argv)
    print('SOMETHING')
    return 0


def target(*args):
    print('SOMETHING2')
    print(args)
    return entry_point, None