from qc_utils import qcmetric
from qc_utils import parsers
from unittest import TestCase
from collections import OrderedDict
from io import StringIO
from unittest.mock import patch

STAR_LOG = '''                                 Started job on | Feb 16 23:45:04
                         Started mapping on |   Feb 16 23:49:02
                                Finished on |   Feb 17 00:16:34
   Mapping speed, Million of reads per hour |   115.09

                      Number of input reads |   52815760
                  Average input read length |   202
                                UNIQUE READS:
               Uniquely mapped reads number |   49542908
                    Uniquely mapped reads % |   93.80%
                      Average mapped length |   201.00
                   Number of splices: Total |   20633562
        Number of splices: Annotated (sjdb) |   20453258
                   Number of splices: GT/AG |   20442117
                   Number of splices: GC/AG |   154577
                   Number of splices: AT/AC |   11212
           Number of splices: Non-canonical |   25656
                  Mismatch rate per base, % |   0.30%
                     Deletion rate per base |   0.02%
                    Deletion average length |   1.51
                    Insertion rate per base |   0.01%
                   Insertion average length |   1.37
                         MULTI-MAPPING READS:
    Number of reads mapped to multiple loci |   2218531
         % of reads mapped to multiple loci |   4.20%
    Number of reads mapped to too many loci |   7303
         % of reads mapped to too many loci |   0.01%
                              UNMAPPED READS:
   % of reads unmapped: too many mismatches |   0.00%
             % of reads unmapped: too short |   1.95%
                 % of reads unmapped: other |   0.03%
                              CHIMERIC READS:
                   Number of chimeric reads |   0
                        % of chimeric reads |   0.00%'''


class TestParsers(TestCase):

    @patch('builtins.open', return_value=StringIO(STAR_LOG))
    def test_parse_starlog(self, mock_open):
        star_log_dict = parsers.parse_starlog('path')
        self.assertEqual(len(star_log_dict), 29)

    def test_raises_error_if_parser_is_invalid(self):
        def invalid_parser(path_to_content):
            return [1, 2, 3]
        with self.assertRaises(TypeError):
            qcmetric.QCMetric('name', 'path_to_content', invalid_parser)
