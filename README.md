
# Chrome Cookie Extraction Without Root

This will print out a user's Chrome cookies. You don't need to have their password or be root to use it. nice nice nice nice nice.

## Features
* Prints all Chrome cookies in sweet sweet JSON
* Works without root or the user's password
* Works on Windows*, Linux, and OS X
* Works if the victim has multiple Chrome Profiles
* Never leaves you on read
* Cooks a mean lasagna
* Compiles to a single binary


## Installation
Requires Python3.6+ to run locally, but the binary it compiles to works anywhere.
```
 pip3 install -r requirements.txt
```

## Usage

To run it locally:
```
   python cookie_crimes.py
```
This will print your Chrome cookies as JSON for the default profile. They're in the right format to be loaded into the [EditThisCookie Chrome Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)

To compile to a single binary:
```
   make
```

Note that the binary created will be for the OS you run `make` on. There's no fancy cross-compiling magic going on here. You'll have to build this on the same OS as you're running it on.

### Multiple Profiles
If you want to extract the Chrome cookies for a profile other than the Default profile, just edit the `PROFILE` variable in `cookie_crimes.py`. This uses some sneaky "writing to `/tmp`" tricks to trick Chrome into reading the cookies for us.


## Cross-platform
\*I absolutely HAVE NOT tested this on Windows and I have no idea if it will work. Sorry all you Michaelsoft Binbows hackers. If you try it and it breaks (hopefully not live on someone's hacked computer during one of your Operations), make a Github Issue, or if you have the courage, a Pull Request.


