import argparse
from glob import glob
from os import path
import json
from os import makedirs


from ranked_vote_report.report import run_report


def generate_reports(raw, elections, out_dir):
    for election_json_file in glob(path.join(elections, '**/*.json'), recursive=True):
        election_dir = path.dirname(election_json_file)
        election_filename, _ = path.splitext(path.basename(election_json_file))

        with open(election_json_file) as fh:
            metadata = json.load(fh)

        od = path.join(out_dir, election_dir)
        makedirs(od, exist_ok=True)

        run_report(metadata, raw, path.join(od, election_filename))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--raw', help='The directory of raw data files.', default='raw')
    parser.add_argument('-e', '--elections', help='The director of election JSON files.', default='elections')
    parser.add_argument('-o', '--out-dir', help='The directory to put the output data.', default='output')

    args = parser.parse_args()
    generate_reports(**vars(args))


if __name__ == '__main__':
    main()