rescue2path
===========
My SD card just died. I managed to salvage 99.52% of it
with the help of ddrescue. However, I didn't know what
files were lost in the remaining 0.48%.

This script takes ddrescue's mapfile as an input and
uses debugfs to find out which files are affected.

Example usage
=============
~~~bash
$ sudo ddrescue -R -d -r3 /dev/sdd rpi.img rpi.img.mapfile

# ... after a while ...

$ sudo losetup -P /dev/loop0 rpi.img
$ fdisk -l /dev/loop0
Disk /dev/loop0: 14.4 GiB, 15489564672 bytes, 30253056 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x86e0dda7

Device       Boot  Start      End  Sectors  Size Id Type
/dev/loop0p1        2048   206847   204800  100M  c W95 FAT32 (LBA)
/dev/loop0p2      206848 30253055 30046208 14.3G 83 Linux

# loop0p2 is the ext4 partition
# 105906176 is its offset in bytes (206848 * 512 from fdisk's output above)
./rescue2path.py rpi.img.mapfile /dev/loop0p2 105906176 > /tmp/r2p.log
~~~

Example output
==============
Block @ 0x128438200 of size 0x1000 bytes:
283523  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-ds1307.ko.gz

Block @ 0x128438400 of size 0x1000 bytes:
283523  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-ds1307.ko.gz

Block @ 0x128439400 of size 0x1000 bytes:
283525  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-ds1390.ko.gz

Block @ 0x12843a400 of size 0x1000 bytes:
283526  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-ds1672.ko.gz

Block @ 0x12843b400 of size 0x1000 bytes:
283528  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-em3027.ko.gz

Block @ 0x12843c400 of size 0x1000 bytes:
283527  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-ds3232.ko.gz

Block @ 0x12843d400 of size 0x1000 bytes:
283527  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-ds3232.ko.gz

Block @ 0x12843e400 of size 0x1000 bytes:
283529  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-fm3130.ko.gz

Block @ 0x12843f200 of size 0x1000 bytes:
283530  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/rtc/rtc-isl12022.ko.gz

Block @ 0x128480000 of size 0x1000 bytes:
283564  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/spi/spi-gpio.ko.gz

Block @ 0x128480200 of size 0x1000 bytes:
283564  /usr/lib/modules/4.14.87-1-ARCH/kernel/drivers/spi/spi-gpio.ko.gz

[...]
