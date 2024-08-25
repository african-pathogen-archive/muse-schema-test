#!/usr/bin/env python3

import argparse
import json
import sys

from urllib.request import urlopen

ANALYSIS_BASE_URL = 'https://raw.githubusercontent.com/overture-stack/SONG/develop/song-server/src/main/resources/schemas/analysis/analysisBase.json'
def fetch_base_schema(url: str = ANALYSIS_BASE_URL) -> str:
    with urlopen(url) as response:
        return response.read().decode('utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge SONG schema with base schema')
    parser.add_argument('--analysis_base_url', help='URL for AnalysisBase schema', default=ANALYSIS_BASE_URL)
    parser.add_argument('schema_file', type=argparse.FileType(), help='Schema definition file')
    parser.add_argument('output_file', type=argparse.FileType('w'), default=sys.stdout, nargs='?', help='Output file')
    args = parser.parse_args()

    base_schema_json = fetch_base_schema(args.analysis_base_url)
    base_schema = json.loads(base_schema_json)

    schema_spec = json.load(args.schema_file)
    if 'schema' not in schema_spec:
        print('Invalid schema file, missing "schema" key', file=sys.stderr)
        sys.exit(1)

    schema = schema_spec['schema']
    for key, value in schema.items():
        if key not in base_schema:
            base_schema[key] = value
        elif isinstance(base_schema[key], dict):
            base_schema[key].update(value)
        elif isinstance(base_schema[key], list):
            base_schema[key].extend(value)
        elif base_schema[key] != value:
            print(f'Conflict in key "{key}"', file=sys.stderr)
            sys.exit(1)

    args.output_file.write(json.dumps(base_schema, indent=2) + '\n')
