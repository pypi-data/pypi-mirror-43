import gzip
import io
import json
import logging
import os

import certifi
import urllib3

from .asyncrecorder import AsyncRecorder
from ..formatters.dict import DictFormatter

logger = logging.getLogger(__name__)

SCOPE_API_ENDPOINT = os.getenv('SCOPE_API_ENDPOINT', 'https://api.codescope.com')


class HTTPRecorder(AsyncRecorder):
    SCOPE_INGEST_ENDPOINT = "%s/%s" % (SCOPE_API_ENDPOINT, 'api/agent/ingest')

    def __init__(self, api_key, metadata=None, **kwargs):
        super(HTTPRecorder, self).__init__(**kwargs)
        self._api_key = api_key
        self.metadata = metadata or {}
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def flush(self, spans):
        payload = {
            "metadata": self.metadata,
            "spans": [],
            "events": [],
        }

        # TODO: limit number of objects sent per request
        for span in spans:
            span_dict = DictFormatter.dumps(span)
            events = span_dict.pop('logs')
            payload['spans'].append(span_dict)
            for event in events:
                event['context'] = span_dict['context']
                payload['events'].append(event)
        self._send(payload)

    def _send(self, body):
        payload_json = json.dumps(body)
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode="wb") as f:
            f.write(payload_json.encode('utf-8'))
        payload_gzip = out.getvalue()

        headers = {
            "Content-Type": "application/json",
            "X-Scope-ApiKey": self._api_key,
            "Content-Encoding": "gzip",
        }
        resp = self.http.request('POST', self.SCOPE_INGEST_ENDPOINT,
                                 headers=headers, body=payload_gzip,
                                 retries=10)
        logger.debug("response from server: %d %s", resp.status, resp.data)
