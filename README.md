# rv-8803-c7
Short python code to read and write to the RTC.
<h2>Description</h2>
This code is a simple easy way to read and initialize time to the RTC of the rv-8803-c7.

<h2>How to use?</h2>
To use this program you have to be running python3. It only accepts 2 arguments in the command line.
<br>
<b>-I</b>  : This is for initializing the RTC with time from the system clock.
<br>
<b>-G</b>  : This is for getting the time from the RTC.
<br>
A proper read will be:
<br>
<b>python3 rv-8803-c7.py -G</b>
<br>
A proper initialization will be:
<br>
<b>python3 rv-8803-c7.py -I</b>
