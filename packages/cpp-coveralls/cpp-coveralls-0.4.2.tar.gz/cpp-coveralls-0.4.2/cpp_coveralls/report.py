from __future__ import absolute_import
from __future__ import print_function

import requests
import json
import os

URL = os.getenv('COVERALLS_ENDPOINT', 'https://coveralls.io') + "/api/v1/jobs"

def post_report(coverage, args):
    """Post coverage report to coveralls.io."""
    response = requests.post(URL, files={'json_file': json.dumps(coverage)},
                             verify=(not args.skip_ssl_verify))
    try:
        result = response.json()
    except ValueError:
        result = {'error': 'Failure to submit data. '
                  'Response [%(status)s]: %(text)s' % {
                      'status': response.status_code,
                      'text': response.text}}
    print(result)
    if 'error' in result:
        return result['error']
    return 0
