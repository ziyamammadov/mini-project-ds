# Mini-project 1: Mutual exclusion and broadcast
The Team: **Ziya Mammadov** and **Konstantin Tenman**

Mini project for the Distributed Systems course where *Ricart & Agrawala* algorithm was implemented.
## To run the program
`./RA_program.sh N` where **N** is amount of processes
## Program video
https://github.com/ziyamammadov/mini-project-ds/blob/main/program_video.mov
## Commands
### list
This command lists all the nodes and its states. *For instance:*
```
Input the command: list
Process 1, state DO-NOT-WANT, time-out 5
Process 2, state DO-NOT-WANT, time-out 5
Process 3, state DO-NOT-WANT, time-out 5
Process 4, state DO-NOT-WANT, time-out 5
Process 5, state DO-NOT-WANT, time-out 5
```
```
Input the command: list
Process 1, state HELD, time-out 5
Process 2, state WANTED, time-out 5
Process 3, state WANTED, time-out 5
Process 4, state WANTED, time-out 5
Process 5, state WANTED, time-out 5
```
### time-p N
This command sets the time-out interval for all processes [5, t], meaning that each process takes its timeout randomly from the interval. This time is used by each process to move between states. For instance,
a process changes from DO-NOT-WANT to WANTED after a time-out, e.g., after 5 seconds. Notice here
that the process cannot go back to DO-NOT-WANT, and can only proceed to HELD once is authorized by 
all the nodes to do so. After the process has going through the steps of accessing and releasing the CS,
then it goes back to the DO-NOT-WANT, where the time-out can be once again trigger to request access
to the CS.
```
Input the command: time-p 11  
Setting the time-out of 11 to the processes
Input the command: list
Process 1, state WANTED, time-out 8
Process 2, state WANTED, time-out 8
Process 3, state HELD, time-out 7
Process 4, state WANTED, time-out 5
Process 5, state DO-NOT-WANT, time-out 6
```
### time-cs N
This command sets the time to the critical section. It assigns a time-out for possessing the critical section
and the time-out is selected randomly from the interval (10, t). By default, each process can have the
critical section for 10 second. For instance, $ time-cs 20, sets the interval for time-out as [10, 20] – in
seconds.
```
Input the command: time-cs 5
The value should be more than 10
Input the command: time-cs 13
Setting the time-out of 13 to the critical session
```
### exit
```
Input the command: exit
Program exited  
```
## Credits
https://courses.cs.ut.ee/LTAT.06.007/2022_spring/uploads/Main/Mini-project1-DS2022.pdf
