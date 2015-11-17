## See notes/iOS.md for some info
import plistlib
from flask import Response
import subprocess
import uuid


def sign(profile, key, cert=None, chain=None):
    """
    Converts the provided options to a plist and spawns an openssl instance to sign it

    This sucks, but there's SMIME python crypto libraries that support S/MIME and Python 3
    at the time of this writing. As soon as one exists, I'd like to use it
    """
    if cert is None:
        cert = key
    cmd = ["openssl", "smime", "-sign", "-signer", cert, "-inkey", key, "-nodetach", "-outform",
           "der"]
    if chain is not None:
        cmd.append("-certfile")
        cmd.append(chain)
    openssl = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return openssl.communicate(plistlib.dumps(profile))[0]


def makeConfig(email, config):
    payloads = []
    if "extrapayloads" in config['IOS']:
        payloads = config['IOS']['extrapayloads']
    name, domain = email.split("@")
    domain = domain.split(".")
    domain.reverse()
    domain = ".".join(domain)
    EmailPayloadIdentifier = "%s.email.%s" % (domain, name)
    PayloadIdentifier = "%s.email" % domain
    payloads.append({
        "PayloadType": "com.apple.mail.managed",
        "PayloadVersion": 1,
        "PayloadIdentifier": EmailPayloadIdentifier,
        "PayloadUUID": uuid.uuid4().hex,
        "PayloadEnabled": True,
        "PayloadDisplayName": config['IOS']['PayloadDisplayName'],
        "EmailAccountDescription": config['IOS']['EmailAccountDescription'],
        "PreventMove": True,
        "IncomingMailServerPortNumber": config['MAIL']['imap']['port'],
        "IncomingMailServerHostName": config['MAIL']['imap']['hostname'],
        "IncomingMailServerAuthentication": "EmailAuthPassword",
        "IncomingMailServerUseSSL": True,
        "OutgoingMailServerPortNumber": config['MAIL']['smtp']['port'],
        "OutgoingMailServerHostName": config['MAIL']['smtp']['hostname'],
        "OutgoingMailServerAuthentication": "EmailAuthPassword",
        "OutgoingMailServerUseSSL": True,
        "EmailAccountType": "EmailAccountType",
        "OutgoingPasswordSameAsIncomingPassword": True
    })
    profile = {
        'PayloadUUID': uuid.uuid4().hex,
        'PayloadIdentifier': PayloadIdentifier,
        'PayloadOrganization': config['IOS']['PayloadOrganization'],
        'PayloadRemovalDisallowed': False,
        'PayloadContent': payloads,
        'PayloadVersion': 1,
        'PayloadType': 'Configuration',
        'PayloadScope': 'System'
        }
    if "PayloadDisplayName" in config['IOS']:
        profile['PayloadDisplayName'] = config['IOS']['PayloadDisplayName']
    signed = sign(profile, config['IOS']['key'], config['IOS']['cert'], config['IOS']['chain'])
    response = Response(signed)
    response.headers['Content-Type'] = "application/x-apple-aspen-config"
    response.headers['Content-Disposition'] = "attachment; filename=\"uwave.mobileconfig\""
    return response
