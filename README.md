# Position_List_PIStage

This program provides an opportunity to manipulate PI stage while taking a video from camera in each position. 

![image](https://github.com/tehsinchen/Position_List_PIStage/blob/main/demo/start_demo.gif)


The default PI stages are C-867 and E-518, they can be changed by modifying the serial number:
```
self.sn_entry_1.insert(0, '0120027194')
self.sn_entry_2.insert(0, '120027848')
```
The functions can be combined with this position list by putting at here:
```
time.sleep(1)   # do whatever you want here
```

## Description of functions in position list

### Add:
>Add the current position in the end
### Remove:
>Remove the selected position
### Clean:
>Clean the position list
### Insert:
>Insert the current position before the selected position
### Replace:
>Replace the selected position with the current position
### Go:
>Go the the selected position
### Start:
>See the demo video above. It provide the opportunity to combine the use of PI stage with other instrument like camera.
### Save:
>Save the position list
### Load:
>Load the position list
### Close:
>Close the application
### Relative Position & Update:
>In the case of the sample needs to be taken away from stage for some treatment then put back. Press 'Set ref.' then 'Update' to set the reference position. When the treatment was done and found the reference position, pressing 'Set ref.' and 'Update' again to update the position list to the current sample position.
### Interval:
>The time interval of the cycle when the 'Start' function is working
### Number of loops(cycles):
>If empty, the 'Start' function will continue until the program is closed
