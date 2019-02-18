import argparse
import json
from glob import glob
from os import path, chdir, getcwd

from ranked_vote_report.report import run_report


def rel_glob(pattern, new_dir):
    old_dir = getcwd()
    chdir(new_dir)
    result = glob(pattern, recursive=True)
    chdir(old_dir)
    return result


def generate_reports(raw, elections, out_dir):
    for election_json_file in rel_glob('**/*.json', elections):
        print('Processing {}'.format(election_json_file))
        election_filename, _ = path.splitext(election_json_file)

        with open(path.join(elections, election_json_file)) as fh:
            metadata = json.load(fh)

        run_report(metadata, election_filename, out_dir, raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--raw', help='The directory of raw data files.', default='raw')
    parser.add_argument('-e', '--elections', help='The director of election JSON files.', default='elections')
    parser.add_argument('-o', '--out-dir', help='The directory to put the output data.', default='reports')

    args = parser.parse_args()
    generate_reports(**vars(args))


if __name__ == '__main__':
    main()
