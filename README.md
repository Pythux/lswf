
# installing

in this directory:
> pip install .


--> [follow installing instruction of systemd](https://github.com/Pythux/lswf/tree/master/systemd)


## /tmp in ram

to put /tmp in RAM:
in file /etc/fstab
if not "tmpfs /tmp" exist, add:
> tmpfs   /tmp    tmpfs   defaults,size=4g        0       0

it will put /tmp in RAM, with a maximun of 4 go usable (use only what it need)

to make changes effectives:
> sudo mount -a


# using lswf

#### before scanning the filesysem, you could add path to avoid from the scan:
> lswf scan add-path-to-avoid "~/will/not/be/scanned"

this will avoid the folder in your HOME/will/not/be/scanned

#### scan all filesystem, useful to know what is frequently modified:
> lswf scan

#### show frequently modified and already in RAM:
> lswf show

#### put file or directory in RAM:
> lswf ram <path>

#### put file or directory out of RAM:
> lswf ram --out <path>
