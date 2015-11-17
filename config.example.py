IOS = {
    "EmailAccountDescription": "Email account description",
    "PayloadIdentifier": "com.example.email",
    "PayloadOrganization": "Awesome Email Service",
    "PayloadDisplayName": "Email service config",
    "key": "keys/iOSsigningkey.pem",
    "cert": "keys/iOSsigningkey.pem",
    "chain": "keys/sub.class1.client.sha2.ca.pem",
    "extrapayloads": [  # this is optional, remove the whole thing if you don't want it
        {
            'PayloadEnabled': True,
            'PayloadUUID': 'c21e7f55-eddc-407f-a2e7-9bd73fc2ee46',  # Remember to generate your own!
            'AuthenticationMethod': '',
            'PayloadIdentifier': 'com.example.profiles.wifi',
            'ProxyType': 'None',
            'PayloadDisplayName': 'Example WiFi Connection',
            'Interface': 'BuiltInWireless',
            'EncryptionType': 'WPA',
            'SSID_STR': 'My Clever SSID',
            'HIDDEN_NETWORK': False,
            'Password': 'Super Secure Password',
            'AutoJoin': True,
            'SetupModes': [],
            'PayloadVersion': 1,
            'PayloadType': 'com.apple.wifi.managed'
        }
    ]
}

MAIL = {
    "imap": {
        "port": 993,
        "hostname": "imap.example.net"
    },
    "smtp": {
        "port": 587,
        "hostname": "mail.example.net"
    }
}
