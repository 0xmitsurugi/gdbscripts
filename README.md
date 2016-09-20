# gdbscripts
Python scripts for gdb, reverse engineering oriented

bocbor.py
=========

bocbor means Break On Call and Break On Ret.
With this script, you can break on the next call and/or break on the next
ret.

It has been tested under x86 and x86\_64, but should work for any CPU.

Usage:
------
Save the `bocbor.py` file in any reachable directory. Inside gdb, source it
in order to load the `boc`, `bor` and `go` commands.
Typing boc or bor will print the settings currently in use.

```gdb
$ gdb -nx -q
(gdb) source bocbor.py 
(gdb) boc
Status of Break on Call is off/break
   Change with boc on/off and boc break/print
(gdb) bor
Status of Break on Ret is off/break
   Change with bor on/off and bor break/print
(gdb) boc on
(gdb) boc
Status of Break on Call is on/break
   Change with boc on/off and boc break/print
(gdb)
```

Typing go will run the binary until a Call or a Ret is found:

```gdb
(gdb) file func
Reading symbols from func...(no debugging symbols found)...done.
(gdb) b * main
Breakpoint 1 at 0x400574
(gdb) r
Starting program: /home/mitsurugi/func 

Breakpoint 1, 0x0000000000400574 in main ()
(gdb) go
[+] BreakOnCall is ON: 0x40059b	callq  0x400546 <print_func>
(gdb) boc off
(gdb) bor on
(gdb) go
This is function print_func
abcdefg
[+] BreakOnRet is ON: 0x400573	retq   
(gdb)
```

You can also choose to print only Call/Ret and not breaking:
```gdb
(gdb) boc on
(gdb) boc print
(gdb) bor on
(gdb) bor print
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y

Starting program: /home/mitsurugi/func 

Breakpoint 1, 0x0000000000400574 in main ()
(gdb) go
[+] BreakOnCall is ON: 0x40059b	callq  0x400546 <print_func>
[+] BreakOnCall is ON: 0x400557	callq  0x400410 <puts@plt>
This is function print_func
[+] BreakOnCall is ON: 0x40056d	callq  0x400420 <printf@plt>
abcdefg
[+] BreakOnRet is ON: 0x400573	retq   
[+] BreakOnCall is ON: 0x40059b	callq  0x400546 <print_func>
[+] BreakOnCall is ON: 0x400557	callq  0x400410 <puts@plt>
This is function print_func
[+] BreakOnCall is ON: 0x40056d	callq  0x400420 <printf@plt>
abcdefg
[+] BreakOnRet is ON: 0x400573	retq   
[+] BreakOnCall is ON: 0x40059b	callq  0x400546 <print_func>
[+] BreakOnCall is ON: 0x400557	callq  0x400410 <puts@plt>
This is function print_func
[+] BreakOnCall is ON: 0x40056d	callq  0x400420 <printf@plt>
abcdefg
[+] BreakOnRet is ON: 0x400573	retq   
[+] BreakOnCall is ON: 0x40059b	callq  0x400546 <print_func>
[+] BreakOnCall is ON: 0x400557	callq  0x400410 <puts@plt>
This is function print_func
[+] BreakOnCall is ON: 0x40056d	callq  0x400420 <printf@plt>
abcdefg
[+] BreakOnRet is ON: 0x400573	retq   
[+] BreakOnRet is ON: 0x4005ab	retq   
[+] BreakOnCall is ON: 0x40050d	callq  0x400480 <deregister_tm_clones>
[+] BreakOnRet is ON: 0x4004b1	retq   
[+] BreakOnRet is ON: 0x40062c	retq   
Python Exception <class 'gdb.error'> No frame is currently selected.: 
Error occurred in Python command: No frame is currently selected.
(gdb)
```

Features
--------
* Only call and ret from the binary are taken into consideration. The
call and ret from linked library doesn't break the flow.
  * This is made by examining the content of `info proc stat`
  * This can be changed by editing the `bocbor.py` file
* This doesn't rely on breakpoint at all. The code just `nexti` the 
instructions until it find a `call` or a `ret` in disasm.

Usage
-----
This script has saved me a lot of time in crackmes challenges. You can
launch different runs of the binary by providing different passwords and
look at function called. By looking at call and ret traces you can learn
a lot from the binary.

Bugs/Enhancement
----------------
* Implement a BOJ (Break On Jump) and a BOT (Break On Test)
* Colors! Colors!
* Integration with tools like gef or peda
* When program finishes, you can see a python exception: this is harmless
* the `go` command already exists inside gdb. If you need it, rename the
`go` command in my script.
