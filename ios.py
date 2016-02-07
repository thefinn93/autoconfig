## See notes/iOS.md for some info
import plistlib
from flask import Response
import subprocess


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
    try:
        unsigned = plistlib.dumps(profile)
    except AttributeError:
        unsigned = plistlib.writePlistToString(profile)
    return openssl.communicate(unsigned)[0]


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
        "PayloadUUID": config['IOS']['EmailPayloadUUID'],
        "PayloadEnabled": True,
        "PayloadDisplayName": config['IOS']['PayloadDisplayName'],
        "EmailAccountDescription": config['IOS']['EmailAccountDescription'],
        "EmailAccountType": "EmailTypeIMAP",
        "EmailAddress": email,
        "IncomingMailServerAuthentication": "EmailAuthPassword",
        "IncomingMailServerHostName": config['MAIL']['imap']['hostname'],
        "IncomingMailServerPortNumber": config['MAIL']['imap']['port'],
        "IncomingMailServerUseSSL": True,
        "IncomingMailServerUsername": email,
        "OutgoingPasswordSameAsIncomingPassword": True,
        "OutgoingMailServerAuthentication": "EmailAuthPassword",
        "OutgoingMailServerHostName": config['MAIL']['smtp']['hostname'],
        "OutgoingMailServerPortNumber": config['MAIL']['smtp']['port'],
        "OutgoingMailServerUseSSL": True,
        "OutgoingMailServerUsername": email,
        "PreventMove": True
    })

    profile = {
        'PayloadUUID': config['IOS']['PayloadUUID'],
        'PayloadIdentifier': PayloadIdentifier,
        'PayloadOrganization': config['IOS']['PayloadOrganization'],
        'PayloadContent': payloads,
        'PayloadVersion': 1,
        'PayloadType': 'Configuration',
        'PayloadScope': 'System'
        }
    if "PayloadDisplayName" in config['IOS']:
        profile['PayloadDisplayName'] = config['IOS']['PayloadDisplayName']
    key = {"key": None, "cert": None, "chain": None}
    for item in key.keys():
        if type(config['IOS'][key]) == dict:
            if domain in config['IOS'][item]:
                key[item] = config['IOS'][item][domain]
            else:
                key[item] = config['IOS'][item]['default'].format(domain=domain)
        else:
            key[item] = config['IOS'][item].format(domain=domain)
    signed = sign(profile, key['key'], key['cert'], key['chain'])
    response = Response(signed)
    response.headers['Content-Type'] = "application/x-apple-aspen-config"
    response.headers['Content-Disposition'] = "attachment; filename=\"uwave.mobileconfig\""
    return response
