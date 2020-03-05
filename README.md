
# Chrome Cookie Extraction Without Root

This will print out a user's Chrome cookies. You don't need to have their password or be root to use it. nice nice nice nice nice.

If you are not the kind of person who regularly gets the ability to execute code on other people's computers, you probably don't care about this.

## Features
* Prints all Chrome cookies in sweet sweet JSON
* Works without root or the user's password
* Works on Windows, Linux, and macOS
* Get cookies fom any Chrome Profile
* Never leaves you on read
* Cooks a mean lasagna
* Compiles to a single binary

## Metasploit module

For ezmode #ethical #hacking, please direct your meterpreter session to https://github.com/rapid7/metasploit-framework/blob/9616a9f79de0b22bfd142f12affd74cecbbd4413/documentation/modules/post/multi/gather/chrome_cookies.md

## Blog post
Read the full details at https://mango.pdf.zone/stealing-chrome-cookies-without-a-password

## Installation
Requires Python3.6+ to run locally, but the binary it compiles to works anywhere.
```
 pip3 install -r requirements.txt
```

## Usage

### Windows and Linux
To run it locally:
```
   python cookie_crimes.py
```
This will print your Chrome cookies as JSON for the default profile. They're conveniently in the right format to be loaded into the [EditThisCookie Chrome Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)

To compile to a single binary:
```
   make
```

Note that the binary created will be for the OS you run `make` on. There's no fancy cross-compiling magic going on here. You'll have to build this on the same OS as you're running it on.

### macOS

For whatever reason, running Chrome with `--headless` has allowed reading of cookies from headful Chrome on-and-off over the last few years as changes to Chrome are made. This has caused the `headless` method to sometimes not work on macOS. 
Instead, you can run:
```
./cookie_crimes_macos.sh
```

##### Formatting for EditThisCookie
Chrome's cookie format stores domains with leading dots (e.g. `.google.com`), and so to import _all_ cookies into Chrome via the EditThisCookie Chrome Extension, you'll need to remove the leading dots. You can do this via the following Enterprise Grade bash script:

```
cat cookies.json | ./format_for_editthiscookie.sh
```

##### How it works
It works by quickly killing and restarting Chrome, and attaching remote debugging to the new Chrome session with `--restore-last-session`. This does have the downside of making the Chrome window look like it crashed for about 0.5s (it did lol) and reloading all tabs. But hey, the user will probably just assume their Chrome crashed and restored itself.

Extra crispy thanks to [@IAmMandatory](https://twitter.com/iammandatory) for sharing this trick `<3`

`cookie_crimes_macos.sh` will also download, execute, and delete a [websocat](https://github.com/vi/websocat) binary to make the websocket request.

### Multiple Profiles
If you want to extract the Chrome cookies for a profile other than the Default profile, just edit the `PROFILE` variable in `cookie_crimes.py`. This uses some sneaky "writing to `/tmp`" tricks to trick Chrome into reading the cookies for us.

## How it works

### Headless Chrome and `user-data-dir`
Headless (no window is rendered) Chrome is allowed to specify a `user-data-dir`. This directory contains cookies, history, preferences, etc. By creating a new headless Chrome instance, and specifying the `user-data-dir` to be the same as the victim's, your headless Chrome instance will authenticate as the vicitm.

### Remote debugging
From here, we just use a normal (but extremely forbidden and undocumented) feature of Chrome: the Remote Debugging protocol. This is how Chrome Developer Tools communicate with Chrome. Once your headless Chrome (with remote debugging enabled) instance is running, this code just executes remote debugging commands to print the user's cookies for all websites in plaintext.

You can fully control Chrome at this point, taking any action the user could take.


### closing ceremony
don't do crimes with this please

