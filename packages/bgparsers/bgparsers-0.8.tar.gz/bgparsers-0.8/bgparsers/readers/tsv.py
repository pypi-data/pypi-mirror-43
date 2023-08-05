import logging

from bgparsers.readers.common import __base_parser, __open_file

logger = logging.getLogger("bgparsers")


def __known_headers(header, schema):
    h_lower = header.lower()
    return [(field, method) for valid_headers, field, method in schema if h_lower in valid_headers]


def head(line, schema, extra=None, required=None):
    header = []
    extra_header = []
    for i, h in enumerate(line):
        known = __known_headers(h, schema)
        if len(known) > 0:
            for field, method in known:
                header.append((field, method, i))
        else:
            extra_header.append((h, str, i))

    inferred_header = len(header) == 0
    if inferred_header:
        # TODO Infer the header from the values of the first line
        raise NotImplementedError("We need a header")

    if extra is not None:

        # TODO Check header collision
        if isinstance(extra, list):
            header += [h for h in extra_header if h[0] in extra]
        else:
            header += extra_header

    if required is not None and not (set(required) <= set([h[0] for h in header])):
        raise SyntaxError('Missing fields in file header. Required fields: {}'.format(required))

    return header, inferred_header


def parser(file, schema, header=None, extra=None, required=None):
    """
    Read a tsv file.
    The header of the file is read and matched against the schema.
    All fields in the schema and in the header of the file are returned;
    those in required must be present in the file header, and
    those in extra are only return if present in the file.

    Args:
        file: file to be read
        schema (list): schema of the known fields to be read
        header (list, optional): header to be used (should contain a tuple for each column as the schema)
        extra (list, optional): headers (not in the schema) to be returned if not present
        required (list, optional): headers that must be present

    Returns:

    """
    fd, close = __open_file(file, "rt")
    for l, line in __base_parser(fd):

        # Initialize header
        if header is None:
            header, inferred_header = head(line, schema, extra=extra, required=required)
            if not inferred_header:
                continue

        try:
            row = {h[0]: h[1](line[h[2]]) for h in header}
        except (ValueError, IndexError) as e:
            logger.warning("Error parsing line %d %s (%s %s %s)", l, file, e, line, header)
            continue

        yield row

    if close:
        fd.close()
