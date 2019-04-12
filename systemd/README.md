
# installation systemd part:

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

if you want to use the service now:
```
systemctl --user start lswf-load.service
systemctl --user start lswf-save.timer
systemctl start lswf-save_at_shutdown.service
```
