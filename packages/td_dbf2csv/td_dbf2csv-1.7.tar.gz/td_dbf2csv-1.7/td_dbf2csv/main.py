#!/usr/bin/env python
# coding: utf-8
import os
import re
import csv
import sys
import glob
import struct
import logging
import argparse
import datetime

from dbfread import DBF, FieldParser

from io import open
from builtins import str


class TranslatingDataFieldParser(FieldParser):
    def parseF(self, field, data):
        """Parse float field and return float or None"""
        # In some files * is used for padding.
        data = data.strip().strip(b'*')

        if data:
            try:
                return float(data)
            except ValueError:
                logging.debug('Unable to parse bad float in parseF')
                return None
        else:
            return None

    def parseN(self, field, data):
        """Parse numeric field (N)

        Returns int, float or None if the field is empty.
        """
        # In some files * is used for padding.
        data = data.strip().strip(b'*')

        try:
            return int(data)
        except ValueError:
            if not data.strip():
                return None
            else:
                # Account for , in numeric fields
                try:
                    return float(data.replace(b',', b'.'))
                except ValueError:
                    logging.debug('Unable to parse bad float in parseN')
                    return None

    def parseL(self, field, data):
        """Parse logical field and return True, False or None"""
        if data in b'TtYy':
            return True
        elif data in b'FfNn':
            return False
        elif data in b'? ':
            return None
        else:
            # Todo: return something? (But that would be misleading!)
            logging.debug('Illegal value for logical field')
            # screw it--I'm returning something anyway. - Caleb
            # raise ValueError(message.format(data))
            return None

    def parseD(self, field, data):
        """Parse date field and return datetime.date or None"""
        try:
            return datetime.date(int(data[:4]), int(data[4:6]), int(data[6:8]))
        except ValueError:
            if data.strip(b' 0') == b'':
                # A record containing only spaces and/or zeros is
                # a NULL value.
                return None
            else:
                logging.debug('Unable to parse garbage date')
                return None


def get_args():
    """Get CLI arguments and options"""
    parser = argparse.ArgumentParser(
        prog='td-td_dbf2csv',
        description='small utility to convert simple *.DBF files to *.CSV'
    )
    parser.add_argument('input')
    parser.add_argument('output', nargs='?', default=None)

    parser.add_argument('-ie', '--input-encoding',
                        default='cp850',
                        help='charset of *.dbf files (default: cp850)')
    parser.add_argument('-oe', '--output-encoding',
                        default='utf8',
                        help='charset of *.csv files (default: utf8)')
    parser.add_argument('-q', '--quoting-mode',
                        choices=('minimal', 'all', 'non-numeric', 'none'),
                        default='minimal',
                        help='quoting mode for csv files (default: minimal)')
    parser.add_argument('-d', '--delimiter-char',
                        default=',',
                        help='delimiter char for csv files (default: ",")')
    parser.add_argument('-e', '--escape-char',
                        default='\\',
                        help='escape char for csv files (default: "\\")')
    parser.add_argument('-s', '--stop-at-memo-sep',
                        action='store_true',
                        help='instruct the reader to stop at the memofile separator byte (\\x1a)')
    return parser.parse_args()


def __convert(input_file_path, output_file, args):
    def encode_decode(x):
        """
        DBF returns a unicode string encoded as args.input_encoding.
        We convert that back into bytes and then decode as args.output_encoding.
        """
        if x is None:
            return ''
        if not isinstance(x, str):
            # DBF converts columns into non-str like int, float
            x = str(x)
        return x.encode(args.input_encoding).decode(args.output_encoding)

    try:
        input_reader = DBF(input_file_path,
                           encoding=args.input_encoding,
                           ignore_missing_memofile=True,
                           parserclass=TranslatingDataFieldParser,
                           stop_at_memofile_separator=args.stop_at_memo_sep)

        output_writer = csv.DictWriter(output_file,
                                       quoting=args.quoting,
                                       escapechar=args.escape_char,
                                       delimiter=args.delimiter_char,
                                       fieldnames=[encode_decode(x) for x in input_reader.field_names])

        output_writer.writeheader()
        row_exceptions = 0
        for record in input_reader:
            try:
                row = {encode_decode(k): encode_decode(v) for k, v in record.items()}
                output_writer.writerow(row)
            except (UnicodeDecodeError, LookupError):
                row_exceptions += 1
                continue
        if row_exceptions:
            logging.error('Number of rows skipped due to encoding errors: %d' % row_exceptions)

    except (UnicodeDecodeError, LookupError):
        logging.error('Error: Unknown encoding in header')
        exit(0)
    except UnicodeEncodeError:
        logging.error('Error: Can\'t encode to output encoding: {}\n'.format(
            args.to_charset))
        exit(0)
    except struct.error:
        logging.error('Error: Bad input file format: {}\n'.format(
            os.path.basename(input_file_path))
        )
        exit(0)


def process_directory(input_dir_path, output_dir_path, args):
    if not output_dir_path:
        output_dir_path = input_dir_path

    input_files = [f for f in glob.glob('{}/*'.format(input_dir_path)) if re.match('^.*\.dbf$', f, flags=re.IGNORECASE)]

    if not input_files:
        exit(0)

    if output_dir_path != input_dir_path:
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

    for input_file_path in input_files:
        output_file_path = '{}/{}.csv'.format(
            output_dir_path,
            os.path.splitext(os.path.basename(input_file_path))[0]
        )
        process_file(input_file_path, output_file_path, args)


def process_file(input_file_path, output_file_path, args):
    if output_file_path:
        with open(output_file_path, 'w', encoding=args.output_encoding) as output_file:
            __convert(input_file_path, output_file, args)
    else:
        __convert(input_file_path, sys.stdout, args)


def main():
    sys.tracebacklimit = 0

    args = get_args()

    if args.quoting_mode == 'minimal':
        args.quoting = csv.QUOTE_MINIMAL
    elif args.quoting_mode == 'all':
        args.quoting = csv.QUOTE_ALL
    elif args.quoting_mode == 'non-numeric':
        args.quoting = csv.QUOTE_NONNUMERIC
    elif args.quoting_mode == 'none':
        args.quoting = csv.QUOTE_NONE

    if os.path.isdir(args.input):
        process_directory(args.input, args.output, args)
    elif os.path.isfile(args.input):
        process_file(args.input, args.output, args)


if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

    try:
        main()
    except KeyboardInterrupt:
        pass
