# Parser functions


def parse_starlog(path_to_log):
    """Parse star logfile into a dict.
    Args:
        path_to_log: filepath containing the star run log
    Returns:
        dict that contains metrics from star log
    """
    qc_dict = {}
    with open(path_to_log) as f:
        for line in f:
            if '|' in line:
                tokens = line.split('|')
                qc_dict[tokens[0].strip()] = tokens[1].strip()
    return qc_dict
