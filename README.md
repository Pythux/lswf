
# installing:




## /tmp in ram:

put something in RAM:
in /etc/fstab
if not "tmpfs /tmp" exist, add:
> tmpfs   /tmp    tmpfs   defaults,size=4g        0       0

it will put /tmp in RAM, with a maximun of 4 go usable (use only what it need)

to make changes effectives:
> sudo mount -a


#### search what could go in RAM:
> lswf scan

#### show frequently modified and already in RAM:
> lswf show

#### put file or directory in RAM:
> lswf ram <path>

#### put file or directory out of RAM:
> lswf ram --out <path>
