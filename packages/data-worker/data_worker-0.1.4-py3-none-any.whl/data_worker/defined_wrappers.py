from data_worker.wrappers.alpha_vantage_wrapper import AlphaVantageWrapper
from data_worker.wrappers.quandl_wrapper import QuandlWrapper

# TODO: Automatically create wrappers
# ############################################################
# TO BE MANUALLY ENTERED
# ############################################################

wrappers = {
    'Alpha Vantage': AlphaVantageWrapper,
    'Quandl': QuandlWrapper
}

# TODO: load API meta data secruely
meta_data = {
    'Alpha Vantage': {'key': 'FMW3UA5PVDR6B9KS'},
    'Quandl': {'key': 'DfJwjc46qz6zsVS9ZgPU'}
}

# ############################################################


def _get_alt_names(name):
    names = [name, name.upper(), name.lower()]

    if ' ' in name:
        no_spaces = [x.replace(' ', '') for x in names]
        underscores = [x.replace(' ', '_') for x in names]
        names += no_spaces + underscores

    letters = ''.join(x[0] for x in name.split(' '))
    letters = [letters, letters.lower()]

    names += letters

    return names


alt_names = {
    name: _get_alt_names(name)
    for name in wrappers.keys()
}

names = list(wrappers.keys())
for i, name1 in enumerate(names):
    for j, name2 in enumerate(names):
        if i == j:
            continue
        duplicates = set(alt_names[name1]).intersection(set(alt_names[name2]))
        assert len(duplicates) == 0, "Duplicate alternative names between \'{}\' and \'{}\'.".format(name1, name2)
