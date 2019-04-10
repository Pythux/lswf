
## installing:

#### generating systemd_to_install directory:

activate your **python env** that will run this programme, then:
```
python3 install.py
cd systemd_to_install
```

#### copying all the services:
```
cp lswf-load.service ~/.config/systemd/user/
cp lswf-save.service ~/.config/systemd/user/
cp lswf-save.timer ~/.config/systemd/user/

sudo cp lswf-save_at_shutdown.service /etc/systemd/system
```

you could now delete the directory "systemd_to_install"


#### enabling all the services:
```
systemctl enable --user lswf-load.service
systemctl enable --user lswf-save.timer

systemctl enable lswf-save_at_shutdown.service
```

## installation complete, complementary information below:

if you want to run it now:
```
systemctl --user start lswf-load.service
systemctl --user start lswf-save.timer
systemctl start lswf-save_at_shutdown.service
```

#### creating a process that take more than 5s to run at shutdown:

##### solution:
in **/etc/systemd/system**: (Local configuration), [here are all systemd path](https://www.freedesktop.org/software/systemd/man/systemd.unit.html#Unit%20File%20Load%20Path)
```
[Unit]
Description=Test wait at shutdown

[Service]
Type=oneshot
RemainAfterExit=true
ExecStop=/full/path/python /script/wait_20s.py
TimeoutSec=50
[Install]
WantedBy=multi-user.target
```

###### work with or without:
```
Conflicts=shutdown.target
Before=shutdown.target
```

The same .service in **~/.config/systemd/user**  
TimeoutSec= is not taken into account, not leting enouth time for a +5s ExecStop script

executables in:
**/usr/lib/systemd/system-shutdown/**
[doc](https://www.freedesktop.org/software/systemd/man/systemd-halt.service.html) [stackexchange](https://unix.stackexchange.com/questions/347306/how-to-execute-scripts-in-usr-lib-systemd-system-shutdown-at-reboot-or-shutdow/347333#347333)

running at the end of shutdown, when the filesystem is unmounted
(could be remounted)
