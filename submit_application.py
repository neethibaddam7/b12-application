import os
import json
import hmac
import hashlib
import urllib.request
from datetime import datetime, timezone


SIGNING_SECRET = os.environ["B12_SIGNING_SECRET"].encode("utf-8")
SUBMISSION_URL = "https://b12.io/apply/submission"


def iso_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


payload = {
    "timestamp": iso_timestamp(),
    "name": "Neethi Baddam",
    "email": "neethibaddam@gmail.com",
    "resume_link": "https://www.linkedin.com/in/nithib-nithib-881531256/",
    "repository_link": os.environ["GITHUB_REPOSITORY_URL"],
    "action_run_link": f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
}

body = json.dumps(
    payload,
    separators=(",", ":"),
    sort_keys=True,
).encode("utf-8")

signature = hmac.new(
    SIGNING_SECRET,
    body,
    hashlib.sha256,
).hexdigest()

request = urllib.request.Request(
    SUBMISSION_URL,
    data=body,
    method="POST",
    headers={
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}",
    },
)

try:
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)

        if result.get("success") is True:
            print(f"Submission receipt: {result['receipt']}")
        else:
            raise RuntimeError(f"Submission failed: {response_body}")

except Exception as error:
    print(f"Error submitting application: {error}")
    raise


