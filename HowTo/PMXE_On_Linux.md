# PMXE on Linux

As of right now (Mar 17 2022), I haven't tested this method enough to say that it works flawlessly, but I've at least been able to get PMXE to launch and open a model.

Trying to use PMXE on Linux will give errors, at least when using the default Wine version. I've been able to get past these errors (specifically, ``Application requires child window rendering, which is not implemented yet!``) by using Proton Experimental. To do this, follow these steps (or something else, like using Lutris, if you know what you're doing):

- Install Steam if you haven't already.
- Install protontricks. It should be in your package manager; if not, you can alternatively use winetricks and point it to the prefix in a path like ``/home/selplacei/.local/share/steam/steamapps/compatdata/123456/pfx`` (make sure the ID matches the PMXE "game").
- Download PMXE. For me, both the English 0.2.2.2 and the Japanese 0.2.5.7 versions work.
- If you haven't already, enable Steam Play for all titles. You can do this by going to Steam, clicking "Steam" at the top, then "Settings...", "Steam Play", and checking "Enable Steam Play for supported titles" and "Enable Steam Play for all other titles".
- Find where the PMXE executable is. In my case, it's in ``/home/selplacei/MikuMikuDance/PMXE/PmxEditor.exe``.
- Go to Steam, click "Games" at the top, click "Add a Non-steam Game to My Library...", click "BROWSE...", and find the PMXE executable.
- Right click on the newly created "game" in your library (it may be at the very bottom of the list), then click "Properties...".
- Make sure that the ``Target`` and ``Start In`` paths are correct, and ``Launch options`` is empty. They could be wrong if your PMXE path contained spaces.
- Click on "COMPATIBILITY", check "Force the use of a specific Steam Play compatibility tool", and choose Proton Experimental.
- Close this window and click "PLAY". I got the error ``Couldn't initialize Direct3D`` - the next steps will fix that.
- Close PMXE.
- Open a terminal and run ``protontricks --gui``. Choose PMXE, then "Select the default wineprefix".
- Install dxvk: choose "Install a Windows DLL or component", then scroll down and check ``dxvk`` (without any extra numbers attached), and press OK until it comes back to the previous screen.
- Install Japanese fonts: choose "Install a font", then choose the desired font(s) - for reliability, I suggest ``cjkfonts``. Click "OK" until it's done, then close protontricks.
- At this point, you should be able to launch PMXE from Steam without any problem.

## Giving PMXE access to the filesystem

By default, Steam's security settings prevent Steam Play applications from seeing your main filesystem, which almost certainly includes all your MMD files. To fix this, you will need to set an environment variable to launch Steam with. First, figure out which folders PMXE will need to access; mine are all under ``/home/selplacei``, so I will give PMXE access to that whole directory. (Note that you cannot just set ``/`` as the directory for various reasons, including even more security measures by Steam. However, you can use ``/mnt``). The environment variable in question is ``STEAM_COMPAT_MOUNTS`` - simply set it to the path, i.e. ``/home/selplacei`` in this case.

There are many ways to do this. The simplest one is to just launch Steam from the terminal using ``STEAM_COMPAT_MOUNTS=/home/selplacei steam``. You can also edit Steam's .desktop file (usually in /usr/share/applications) - this will enable such access to all Proton applications at all times, so be careful. Another way is to add ``export STEAM_COMPAT_MOUNTS=/home/selplacei`` to your ``~/.profile``, which will also give access to all Proton applications at all times. Finally, if you're really concerned about security, you can duplicate Steam's .desktop file, put it in ``~/.local/share/applications``, add the environment variable to it, and prefix the command with ``killall steam && `` - then use this whenever you need PMXE.

## Fixing scaling issues

In certain cases, imperfect scaling mechanisms result in some elements of the PMXE gui being invisible; for example:

![Text boxes and labels overflow their widget area.](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/4_1.jpg?raw=true)

This issue can be solved by editing the ``HKEY_CURRENT_USER/Control Panel/Desktop`` registry value. For example, using protontricks:

- Open protontricks and choose PMXE's prefix.
- Go to "Choose default wineprefix", then "Run regedit".
- Navigate to ``HKEY_CURRENT_USER/Control Panel/Desktop`` (click on the Desktop folder itself).
- Double-click ``LogPixels``.
- Change the value to something lower - for me, 57 works fine. Keep in mind that this number is hexadecimal.
- Click "OK" and close protontricks along with regedit.

This value can technically be changed in winecfg, but that only allows increasing it, while we want the opposite.
