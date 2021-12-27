from ale.md_config_reader import parse_config
import pickle

def pickle_options():
    options = []

    filenames = ['test/config_Cu.yaml', 'test/config_Ar.yaml']

    for filename in filenames:
        with open(filename, 'r') as f:
            option = parse_config(f)
            options.append(option)


    #print(options)


    with open('options_pickle', 'wb+') as f:
        pickle.dump(options, f)


if __name__=="__main__":
    pickle_options()
