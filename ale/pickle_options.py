from ale.md_config_reader import config_parser
import pickle

def pickle_options():
    options = []

    filenames = ['test/config_Cu.yaml', 'test/config_Ar.yaml']

    for filename in filenames:
        with open(filename, 'r') as f:
            option = config_parser(f)
            options.append(option)


    #print(options)


    with open('options_pickle', 'wb+') as f:
        pickle.dump(options, f)


if __name__=="__main__":
    pickle_options()
