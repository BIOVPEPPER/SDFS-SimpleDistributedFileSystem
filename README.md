# CS425_MP3_LiYao


## Join SDFS
At each machine, nder the repo folder, execute command
```
./commands.sh join
```
to join SDFS. You will need superuser privilege to for this.

Only when at VM1, also execute command
```
python3 Coordinator.py 
```
Since VM1 is the default Coordinator.

## Put file into SDFS 
At any machine that have joined SDFS, execute command
```
./commands.sh put localfilename sdfsfilename
```


## Get file from SDFS
At any machine that have joined SDFS, execute command
```
./commands.sh sdfs sdfsfilename  localfilename
```
The  fetched file will be written into `localfilename`.

## Delete file in SDFS
At any machine that have joined SDFS, execute command
```
./commands.sh delete sdfsfilename
```

## List VMs storing a given file
At any machine that have joined SDFS, execute command
```
./commands.sh ls sdfsfilename 
```

## List SDFS files stored on current VM
At any machine that have joined SDFS, execute command
```
./commands.sh store 
```

## Get latest versions of a file
At any machine that have joined SDFS, execute command
```
./commands.sh get_version sdfsfilename num-version localfilename
```
The latest `num-version` versions of `sdfsfilename` will be written into `localfilename`, seperated by delimiters.
