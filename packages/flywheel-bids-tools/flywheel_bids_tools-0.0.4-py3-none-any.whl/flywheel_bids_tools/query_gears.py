import pandas as pd
import flywheel
import warnings
import argparse
from tabulate import tabulate
from pandas.io.json.normalize import nested_to_record


def collect_gear_config(gear_id, client):
    '''
    Collects the gear's configuration and inputs
    '''
    gear = client.get_gear(gear_id)
    name = gear['gear']['name']
    label = gear['gear']['label']
    description = gear['gear']['description']
    inputs = nested_to_record(gear.gear.inputs)
    config = nested_to_record(gear.get_default_config())
    return({'name': name, 'inputs': inputs, 'config': config, 'label': label, 'description': description})


def main():


    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fw = flywheel.Client()
        assert fw, "Your Flywheel CLI credentials aren't set!"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-name", "--gear-name",
        dest='name',
        help="Shorthand name of the gear on Flywheel",
        required=False
    )

    args = parser.parse_args()
    if args.name:
        print()
    else:
        gears = fw.gears()
        gears_table = [nested_to_record(g.to_dict(), sep='_') for g in gears]
        df = pd.DataFrame(gears_table)
        df = df.filter(regex=r'gear_label$|gear_name$|^category$', axis = 1)
        print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == '__main__':
    main()
