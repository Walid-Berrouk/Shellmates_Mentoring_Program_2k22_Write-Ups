# lies

## Description

> I asked my friend where is he, he lied to me through this picture, can you find the datetime of the pic and prove me right?
> Flag format shellmates{YY:MM:DD}

## Tags

easy

## Write-Up

So basically in this challenge we need to have the original picture creation date, we can find that from `exiftool` command :


```
exiftool pic.jpeg
```

```
ExifTool Version Number         : 12.49
File Name                       : pic.jpeg
...
Scale Factor To 35 mm Equivalent: 6.5
Shutter Speed                   : 1/40
Create Date                     : 2021:10:25 07:48:37.144
Date/Time Original              : 2021:10:25 07:48:37.144
Modify Date                     : 2021:10:25 07:48:37.144
...

```


## Flag

shellmates{2021:10:25}