## README


__Read /var/log/apt/history.log.* and display it usefully__


Take a look in CHANGELOG.md.

Try to not fill to much memory, for small devices. So often read files, event if it's slower.

Please, if you want something more complete, look at https://github.com/terminalforlife/apt-undo-install/blob/master/apt-undo-install side

## Install (without pain)

 * *After clone from GIT* :
    * Become root user
    * Copy **apt-histo.py** in **/usr/local/bin**
    * Copy **Show_datas.py** and **Read_histo.py** in **/usr/local/lib/python3.X/dist-packages**


 * *After Pypi install* :
    * Become root user
    * Make a link of **apt-histo.py** from **/usr/local/lib/python3.X/dist-packages/apt-histo/apt-histo.py** to **/usr/local/bin/apt-histo.py**

        **ln -s /usr/local/lib/python3.X/dist-packages/apt-histo/apt-histo.py /usr/local/bin/apt-histo.py**
