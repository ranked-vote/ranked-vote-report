import json
from os import path
from typing import List, Dict, Set

from ranked_vote.analysis.final_by_first import FinalByFirst
from ranked_vote.analysis.first_alternate import FirstAlternates
from ranked_vote.analysis.pairwise_preferences import PreferenceMatrix
from ranked_vote.ballot import Candidate
from ranked_vote.format import read_ballots
from ranked_vote.methods import METHODS
from ranked_vote_import.bin.import_rcv_data import import_rcv_data


def graph_to_dict(graph: Dict[Candidate, Set[Candidate]]) -> List[Dict]:
    return [
        {
            'source': str(c),
            'edges': [str(e) for e in edges]
        }
        for c, edges in graph.items()
    ]


def run_report(metadata, base_dir, output_name, force=False):
    files = [path.join(base_dir, f) for f in metadata['files']]
    print(output_name)

    normalized_data_filename = output_name + '.normalized.csv.gz'

    if not path.exists(normalized_data_filename) or force:
        import_rcv_data(metadata['format'], files, normalized_data_filename, True)

    with open(output_name + '.normalized.json') as meta_fh:
        meta = json.load(meta_fh)

    # TODO: use ballots for candidates
    candidates = [Candidate(c) for c in meta['candidates']]

    ballots = list(read_ballots(normalized_data_filename))

    tabulator = METHODS[metadata['tabulation']](ballots)

    matrix = PreferenceMatrix(candidates, ballots)
    first_alternates = FirstAlternates(candidates, ballots)
    final_by_first = FinalByFirst(tabulator)

    result = {
        'meta': meta,
        'candidates': [str(c) for c in tabulator.candidates],
        'rounds': [r.to_dict() for r in tabulator.rounds],
        'smith_set': [str(c) for c in matrix.smith_set],
        'condorcet': str(matrix.condorcet_winner),
        'graph': graph_to_dict(matrix.graph),
        'pairwise': matrix.to_dict_list(),
        'first_alternates': first_alternates.to_dict_list(),
        'final_by_first': final_by_first.to_dict_list()
    }

    with open(output_name + '.json', 'w') as ofh:
        json.dump(result, ofh, indent=2)
