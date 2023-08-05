from defined_wrappers import wrappers, meta_data, alt_names


def get_wrapper(target_wrapper):
    sources_string = '\n'
    for wrapper_name in wrappers:
        wrapper_alt_names = alt_names[wrapper_name]
        if target_wrapper in wrapper_alt_names:
            return wrappers[wrapper_name](wrapper_name, wrapper_alt_names, meta_data[wrapper_name])
        else:
            sources_string += ''.join(
                '  {}: {}\n'.format(wrapper_name, ', '.join(['\'{}\''.format(x) for x in alt_names]))
            )

    raise Exception(
        '\'{}\' is not a valid source. Must be one of:\n{}'.format(target_wrapper, sources_string)
    )


def get_wrapper_method(wrapper, target_method):
    if target_method[:4] != 'get_':
        target_method = 'get_' + target_method

    wrapper_methods = [
        getattr(wrapper, method) for method in dir(wrapper)
        if callable(getattr(wrapper, method)) and
        getattr(wrapper, method).__name__[:4] == 'get_'
    ]

    for method in wrapper_methods:
        if method.__name__ == target_method:
            return method

    methods_string = '\n  '.join(['{}()'.format(x.__name__) for x in wrapper_methods])
    methods_string = '\n  ' + methods_string + '\n'

    raise Exception(
        '\'{}\' is not a valid {} method. Must be one of:\n{}'.format(target_method, wrapper.name, methods_string)
    )
