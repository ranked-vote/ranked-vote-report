import json
from os import path, makedirs
from typing import List, Dict, Set

from ranked_vote.analysis.final_by_first import FinalByFirst
from ranked_vote.analysis.first_alternate import FirstAlternates
from ranked_vote.analysis.pairwise_preferences import PreferenceMatrix
from ranked_vote.ballot import Candidate
from ranked_vote.format import write_ballots
from ranked_vote.methods import METHODS
from ranked_vote_import import FORMATS, NORMALIZERS


def graph_to_dict(graph: Dict[Candidate, Set[Candidate]]) -> List[Dict]:
    return [
        {
            'source': str(c),
            'edges': [str(e) for e in edges]
        }
        for c, edges in graph.items()
    ]


def run_report(metadata, output_name, output_base_dir, data_base_dir, force=False):
    params = metadata.get('params', dict())
    files = metadata['files']
    fmt = metadata['format']

    data_out_filename = output_name + '.normalized.csv.gz'
    data_out_full_path = path.join(output_base_dir, data_out_filename)
    report_out_filename = path.join(output_base_dir, output_name + '.json')

    makedirs(path.dirname(data_out_full_path), exist_ok=True)

    if path.exists(data_out_full_path) and path.exists(report_out_filename) and not force:
        print('Nothing to do.')
        return

    reader = FORMATS[fmt](files, params, data_base_dir)

    normalizer = NORMALIZERS[fmt]()

    ballots = [normalizer.normalize(ballot) for ballot in reader]
    write_ballots(data_out_full_path, ballots)

    meta = reader.get_metadata()

    tabulator = METHODS[metadata['tabulation']](ballots)
    candidates = tabulator.candidates

    matrix = PreferenceMatrix(candidates, ballots)
    first_alternates = FirstAlternates(candidates, ballots)
    final_by_first = FinalByFirst(tabulator)

    result = {
        'meta': meta,
        'normalized_ballots': data_out_filename,
        'candidates': [str(c) for c in tabulator.candidates],
        'rounds': [r.to_dict() for r in tabulator.rounds],
        'smith_set': [str(c) for c in matrix.smith_set],
        'condorcet': str(matrix.condorcet_winner),
        'graph': graph_to_dict(matrix.graph),
        'pairwise': matrix.to_dict_list(),
        'first_alternates': first_alternates.to_dict_list(),
        'final_by_first': final_by_first.to_dict_list()
    }

    with open(report_out_filename, 'w') as ofh:
        json.dump(result, ofh, indent=2)
