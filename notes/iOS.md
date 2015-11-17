# Notes for iOS stuff
iOS devices want to download a `.mobileconfig` file in Apple's plist format, signed using S/MIME
with a personal certificate that can be validated using the built in CA list. StartCom's work fine.
Currently `ios.py` generates one that should work to connect to the UWave Radio wifi network. There
doesn't seem to be any python library to do S/MIME that supports Python 3, so it hackily spawns
an openssl process.
Here are some links:
* [Apple's Configuration Profile reference](https://developer.apple.com/library/ios/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html)
* [Apple's Over-the-Air Profile Delivery Concepts](https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/iPhoneOTAConfiguration/OTASecurity/OTASecurity.html)
* [Third party page on how to sign these things](https://wiki.geant.org/display/tcs/Sign+Apple+mobileconfig+files)
* [Collection of example profiles](https://github.com/nmcspadden/Profiles)
