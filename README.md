# Cross-Timezone-Timetable
![Icon](UI/Layouts/Image_assets/ctztt.png?raw=true "CTZTT")
A Time-table cross platform application that allows user to convert timetable from any timezone to another with ease.

## Installation

To run CTZTT, a deb package for debian based linux distributions, and a windows executable are available. 

For the Debian based distributions, navigate to the
deb package directory.

    sudo dpkg -i ctztt.deb

The Windows executable can be run directly.

For other systems, or to prevent a download of desktop application, 
the source code can be executed as described below. Python 3.8 + is required.

    pip install PyQt5
    
Then, run the main script from the downloaded zip file.

    python __main__.py

## Usage

### Editing
The original timetable needs to be created by the user by clicking on the
create button on the home screen. The menu bar in the new editable
Time-table window provides the following functionality:

* Add Schedule  (<kbd>Ctrl</kbd> + <kbd>A</kbd>)
* Delete Schedule (<kbd>Ctrl</kbd> + <kbd>D</kbd>)
* Edit Saved Time-table (<kbd>Ctrl</kbd> + <kbd>L</kbd>)
* Save Time-table (<kbd>Ctrl</kbd> + <kbd>S</kbd>)

### Conversion
Two drop down menus are provided, one representing the current time-zone
while the other represents the target time-zone. The former refers
to the time-zone which the original time-table was made in, while the latter
is that of the shifted time-table required. Press convert to open up 
the shifted read-only time-table

### Display
The shifted time-table is displayed in a non-interactive time-table.

