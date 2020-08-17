# cmus-discord
Discord Rich Presence Support for cmus, including pausing support.

## Dependencies 
* [pypresence](https://pypi.org/project/pypresence/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [next_asyncio](https://pypi.org/project/nest-asyncio/)
* [pustil](https://pypi.org/project/psutil/)

## Installation
Tested and working on Arch Linux 5.8.1, should work on other Unix based operating systems, but I have no way of testing them currently. If you have issues with your system, please create an issue and I can help you.

1. Create the cmus directory in your home folder if it does not exist yet. The [cmus documentation](https://github.com/cmus/cmus/wiki/status-display-programs) opts for `/home/username/.cmus/`, although `/home/username/.config/cmus/` will also work, you will have to specify this later though, so remember your choice. 
```
$ ls ~/.config/cmus
$ ls: cannot access ~/.config/cmus: No such file or directory
$ mkdir ~/.config/cmus
```

2. Clone this repository and move the files to your cmus directory:
```
$ git clone https://github.com/coletonodonnell/cmus-discord.git
$ cd cmus-discord
$ mv * ~/.config/cmus/
```

3. chmod and edit `status_display_program.sh` with your details:
```
$ cd ~/.config/cmus/
$ chmod +x status_display_program.sh
$ vim status_display_program.sh
```
You should see something like:
```
#!/bin/sh
/usr/bin/python3 /home/username/.config/cmus/cmus-discord.py "$*" &
```
Change username with your username, and assuming you are using `~/.config/cmus/` to store this program, then keep that as is. This also assumes that your python executable is located at `/usr/bin/`, if it is not, also change that. 

Note:
If you use other status display programs for cmus, such as cmusfm, please refer to the [cmus documentation](https://github.com/cmus/cmus/wiki/status-display-programs#usage--installation). Support for multiple display programs is as easy as adding an extra line to `status_display_program.sh`:
```
#!/bin/sh
/usr/bin/python3 /home/username/.config/cmus/cmus-discord.py "$*" &
cmusfm "$@" &
```

4. Create and edit the .env file:
```
$ vim .env
```

Add the following:
```
# .env
FULL_DIRECTORY = "/home/username/.config/cmus/"
```

Just like in `status_display_program.sh`, change the username with your username. **This must end with / for the script to work.**

5. Open cmus, and enter the following:
```
:set status_display_program=/home/username/.config/cmus/status_display_program.sh
:save
```
Where username is your username you used before. 

## Notes
This is one of the first actual things I've written, and I am rather new to Python (only about 6-8 months of actual practice.) Please point out any errors and areas of improvement, so that this can run better, and also so that I can further my learning! This can either be through an issue, or a pull request, whatever you feel like. Enjoy! 
