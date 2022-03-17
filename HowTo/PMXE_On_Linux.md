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
