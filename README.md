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
&nbsp;  &nbsp;  Add the current position in the end
### Remove:
&nbsp;  &nbsp;  Remove the selected position
### Clean:
&nbsp;  &nbsp;  Clea the position list
### Insert:
&nbsp;  &nbsp;  Insert the current position before the selected position
### Replace:
&nbsp;  &nbsp;  Replace the selected position with the current position
### Go:
&nbsp;  &nbsp;  Go the the selected position
### Start:
&nbsp;  &nbsp;  See the demo video above. It provide the opportunity to combine the use of PI stage with other instrument like camera.
### Save:
&nbsp;  &nbsp;  Save the position list
### Load:
&nbsp;  &nbsp;  Load the position list
### Close:
&nbsp;  &nbsp;  Close the application
### Relative Position & Update:
&nbsp;  &nbsp;  In the case the sample needs to be taken away from stage for some treatment then put back. Press 'Set ref.' then 'Update' to set the reference position. When the treatment was done and found the reference position, pressing 'Set ref.' and 'Update' again to update the position list to the current sample position.
### Interval:
&nbsp;  &nbsp;  The time interval of the cycle when the 'Start' function is working
### Number of loops(cycles):
&nbsp;  &nbsp;  If empty, the 'Start' function will continue until the program is closed
