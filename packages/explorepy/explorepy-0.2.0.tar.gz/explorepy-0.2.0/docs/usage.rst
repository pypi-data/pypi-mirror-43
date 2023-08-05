=====
Usage
=====

To use explorepy in a project::

	import explorepy


Initialization
^^^^^^^^^^^^^^
Before starting a session, make sure your device is paired to your computer. The device will be shown under the following name: Explore_XXXX,
with the last 4 characters being the last 4 hex numbers of the devices MAC adress

Make sure to initialize the bluetooth connection before starting a recording session or a push to lsl using the following lines::

    explorer = explorepy.Explore()
    explorer.connect(device_name="Explore_XXXX") #Put your device Bluetooth name

Alternatively you can use the device's MAC address::

    explorer.connect(device_addr="XX:XX:XX:XX:XX:XX")

If the device is not found it will raise an error.

Streaming
^^^^^^^^^
After connecting to the device you are able to stream data and print the data in the console.::

    explorer.acquire()


Recording
^^^^^^^^^
Afterwards you are free to start recording to CSV using the following line::

    explorer.record_data(file_name='test')

This will record data in two separate files "test_ExG.csv" and "test_ORN.csv" which contain ExG and orientation data (accelerometer, gyroscope, magnetometer) respectively.
The program will usually stop if files with the same name are detected. If you want to overwrite already existing files, change the line above::

    explorer.record_data(file_name='test', do_overwrite=True)

Labstreaminglayer (lsl)
^^^^^^^^^^^^^^^^^^^^^^^
You can push data directly to LSL using the following line::

    explorer.push2lsl(n_chan=4)

or ::

    explorer.push2lsl(n_chan=8)

It is important that you state the number of channels your device has. (either 4 or 8)
After that you can stream data from other software such as OpenVibe or other programming languages such as MATLAB, Java, C++ and so on. (See `labstreaminglayer <https://github.com/sccn/labstreaminglayer>`_, `OpenVibe <http://openvibe.inria.fr/how-to-use-labstreaminglayer-in-openvibe/>`_ documentations for details).

In case of a disconnect (device loses connection), the program will try to reconnect automatically.


Converter
^^^^^^^^^
It is also possible to extract BIN files from the device via USB. To convert these to CSV, you can use the function bin2csv, which takes your desired BIN file
and converts it to 2 CSV files (one for orientation, the other one for ExG data). Bluetooth connection is not necessary for conversion. ::

    from explorepy.tools import bin2csv
    bin2csv(bin_file)

If you want to overwrite existing files, use::

    bin2csv(bin_file, do_overwrite=True)


