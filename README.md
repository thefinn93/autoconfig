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

# Thunderbrid
Thunderbird autoconfig documentation is [here](https://developer.mozilla.org/en-US/docs/Mozilla/Thunderbird/Autoconfiguration).
