
# Chrome Cookie Extraction Without Root

This will print out a user's Chrome cookies. You don't need to have their password or be root to use it. nice nice nice nice nice.

If you are not the kind of person who regularly gets the ability to execute code on other people's computers, you probably don't care about this.

## Features
* Prints all Chrome cookies in sweet sweet JSON
* Works without root or the user's password
* Works on Windows*, Linux, and OS X
* Works if the victim has multiple Chrome Profiles
* Never leaves you on read
* Cooks a mean lasagna
* Compiles to a single binary


## Blog post
Read the full details at https://mango.pdf.zone/stealing-chrome-cookies-without-a-password

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

## How it works

### Headless Chrome and `user-data-dir`
Headless (no window is rendered) Chrome is allowed to specify a `user-data-dir`. This directory contains cookies, history, preferences, etc. By creating a new headless Chrome instance, and specifying the `user-data-dir` to be the same as the victim's, your headless Chrome instance will authenticate as the vicitm.

### Remote debugging
From here, we just use a normal (but extremely forbidden and undocumented) feature of Chrome: the Remote Debugging protocol. This is how Chrome Developer Tools communicate with Chrome. Once your headless Chrome (with remote debugging enabled) instance is running, this code just executes remote debugging commands to print the user's cookies for all websites in plaintext.

You can fully control Chrome at this point, taking any action the user could take.

### Metasploit module
I'm workin' on it! Check back here when it's done.

### closing ceremony
don't do crimes with this please

