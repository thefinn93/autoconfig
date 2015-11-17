# Autoconfig
An attempt to ease configuration of various things (mostly email) to end users.


## iOS
Currently we can generate signed configuration profiles for iOS devices, as long as you fill out
`config.py` correctly

## Android
Android's built in mail client sucks, so we recommend users use K9 mail, which sucks less but has
no formal autoconfiguration. There [is an open issue about this](https://github.com/k9mail/k-9/issues/777),
in which some users suggest building a K9 export file and sending it to the user, which will cause
K9 to offer to import it. Works pretty well for the first profile, but not as smooth if an email
account has already been configured.

## Thunderbrid
Thunderbird autoconfig documentation is [here](https://developer.mozilla.org/en-US/docs/Mozilla/Thunderbird/Autoconfiguration).


# Configuration
Copy `config.example.py` to `config.py` and edit as needed.

## Signing
Note that for iOS stuff to work, you will need a certificate, ideally one signed by a CA in the iOS
device's trust store. I used [StartSSL](https://www.startssl.com/), a free CA in the iOS root store
that will issue the S/MIME certificates that we need. During signup your browser will automatically
generate one and they will sign it, which is all you need, just be aware that that email will be
displayed on the device during installation. To convert it to `pem` format from the pkcs12 that your
browser will likely export it as, I used this command:

```
openssl pkcs12 -in keys/mycert.p12 -out keys/iOSsigningkey.pem -nodes
```

You will also need to download [this intermediate CA certificate](https://www.startssl.com/certs/class1/sha2/pem/sub.class1.client.sha2.ca.pem)
and put it's path in the config under `IOS.chain`.

## Additional iOS Payloads
There are loads of other things you can do to the iOS device, which can be easily added to the
profile. To do this, use the `IOS.extrapayloads` configuration option, which should be a list of
dicts which represent the various payloads. The example config comes with one to tell the iOS device
about a WiFi network with a simple WPA2 password. [Here](https://github.com/nmcspadden/Profiles) is
a nice set of sample profiles with interesting payloads, and [here](https://developer.apple.com/library/ios/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html)
is the Apple documentation on the different payload types.


# Contributing
I don't have an iOS device, so I proly missed something or messed something up. I test with some of
my more tech-savvy user's devices when I can convince them to let me... Feel free to make pull
requests or file issues.
