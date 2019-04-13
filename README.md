
# installing:

clone this directory and:
 - patcher
 - py_tools
 - py_CRUD_vanilla

install all of them:  
* in the cloned project:
> pip install .

* in the directory that contant the cloned project:
> pip install project_name


--> [follow installing instruction of systemd](https://github.com/Pythux/lswf/tree/master/systemd)


## /tmp in ram:

put something in RAM:
in /etc/fstab
if not "tmpfs /tmp" exist, add:
> tmpfs   /tmp    tmpfs   defaults,size=4g        0       0

it will put /tmp in RAM, with a maximun of 4 go usable (use only what it need)

to make changes effectives:
> sudo mount -a


# using lswf:

#### scan all filesystem, useful to know what is frequently modified:
> lswf scan

#### show frequently modified and already in RAM:
> lswf show

#### put file or directory in RAM:
> lswf ram <path>

#### put file or directory out of RAM:
> lswf ram --out <path>
