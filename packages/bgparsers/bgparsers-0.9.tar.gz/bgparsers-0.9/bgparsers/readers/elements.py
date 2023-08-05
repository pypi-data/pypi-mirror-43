import os

from intervaltree import IntervalTree
from tqdm import tqdm
from collections import defaultdict

from bgparsers.readers import tsv
from bgparsers.readers.common import __count_lines

SCHEMA = [

    # Chromosome
    ({'chromosome', 'chr', 'chrom', 'chromosome_name', '#chrom'}, 'CHROMOSOME',
     lambda c: c.upper().replace('CHR', '').replace('23', 'X').replace('24', 'Y')),

    # Start position
    ({'start', 'start_position', 'chromosome_start', 'begin', 'begin_position', 'chromosome_begin'}, 'START', int),

    # End position
    ({'stop', 'stop_position', 'chromosome_stop', 'end', 'end_position', 'chromosome_end'}, 'END', int),

    # Strand
    ({'strand', 'chromosome_strand'}, 'STRAND',
     lambda s: '-' if s in ['-', '0', '-1'] else '+' if s in ['+', '1', '+1'] else None),

    # Element ID
    ({'element', 'id', 'id_element', 'element_id'}, 'ELEMENT', str),

    # Segment ID
    ({'segment', 'transcript', 'segment_id', 'transcript_id'}, 'SEGMENT', str),

    # Symbol ID
    ({'symbol', 'symbol_id', 'alternative_id'}, 'SYMBOL', str),

]


def elements(file, extra=None, required=None):
    """Yield rows in elements file"""
    return tsv.parser(file, schema=SCHEMA, extra=extra, required=required)


def elements_dict(file, extra=None, required=None, show_progress=True):
    """
    Parse an elements file as a dict where keys are the ELEMENTS
    """

    lines_count = __count_lines(file) if show_progress else None
    required = ['ELEMENT'] if required is None else required
    elements_ = {}
    reader = elements(file, extra=extra, required=required)
    msg = "'{}'".format(os.path.basename(file)) if type(file) == str else ""
    for i, r in enumerate(tqdm(reader, total=lines_count, desc="Parsing elements {}".format(msg).rjust(40),
                               disable=(not show_progress)), start=1):

        r['LINE'] = i
        elements_[r['ELEMENT']] = elements_.get(r['ELEMENT'], []) + [r]

    return elements_


def elements_tree(file):
    """Build a regions tree as a dict with the chromosomes as keys.
    Each interval contains element and line number as data"""
    required_fields = ['CHROMOSOME', 'START', 'END', 'ELEMENT']
    e = elements_dict(file, required=required_fields)
    regions_tree = defaultdict(IntervalTree)
    for i, (k, allr) in enumerate(tqdm(e.items(), total=len(e), desc="Building mapping tree".rjust(40))):
        for r in allr:
            regions_tree[r['CHROMOSOME']][r['START']:(r['END']+1)] = (r['ELEMENT'], r['LINE'])
    return regions_tree

