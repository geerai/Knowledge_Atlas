# OpenAlex Support Email Draft

To:
- `support@openalex.org`

Optional additional contact if relevant to the trial arrangement:
- `support@ourresearch.org`

Subject:
- `OpenAlex API key returns 401 "API key not found"`

Body:

```text
Hello,

We are testing an OpenAlex API key for academic literature discovery and are seeing a consistent authentication failure.

Behavior observed on March 24, 2026:

1. Requests to the OpenAlex API succeed without the key at normal public limits.
2. The same requests fail when the provided key is included as `api_key=...`.

Example working request without key:
https://api.openalex.org/works?search=test&per_page=1&mailto=research@ucsd.edu&filter=type:article

Example failing request with key:
https://api.openalex.org/works?search=test&per_page=1&mailto=research@ucsd.edu&filter=type:article&api_key=REDACTED

Observed response:
401 Unauthorized
{"error":"Invalid or missing API key","message":"API key not found"}

Could you confirm:
1. whether this key is active,
2. whether it is tied to the correct account,
3. whether a different authentication method is required for this trial/premium key,
4. whether the key has expired or not yet been activated.

Thank you.
```

Operational note:
- the current problem appears to be key/account validity, not request formatting
- the same endpoint succeeds immediately when the `api_key` parameter is removed
