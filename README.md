# Open-Labels
A utility to print barcode and other labels on the Bixolon SLP-T400 Label printer on Linux written in Python. It communicates with the printer using the Bixolon SLCS command set via the usb node /dev/usb/lpx, without going through the CUPS printer driver.

It currently can automatically detect the usb node for Bixolon SLP-T400 printer. 

Usage is as follows.

```

        python main.py <label-file> <width-mm> <height-mm> <horizontal-gap-mm> <vertical-gap-mm> <labels-per-row> <paper-width-mm> <lable-count> [<printer-port>]
```

```
        
        1) label-file         : Path to the label file. Must be a black and white 8-bit per pixel BMP file
        2) width-mm           : Width of the label in mm
        3) height-mm          : Height of the label in mm
        4) horizontal-gap-mm  : Horizontal gap between two adjacent labels in mm
        5) vertical-gap-mm    : Vertical gap between two adjacent labels in mm
        6) labels-per-row     : Number of labels per row on the paper.
        7) paper-width-mm     : Width of the label paper in mm
        8) label-x-offset-mm  : Horizontal offset in mm
        9) layel-y-offset-mm  : Vertical offset in mm
        10) label-count       : Number of lables to print
        11) printer-port      : [Optional] printer device path [eg: /dev/usb/lp0]
```

# TODO List

 - [x] Create basic utility
 - [x] Fix bug in printing 2 labels when 3 labels are in a row
 - [ ] Create GUI 
 - [ ] Create Base64 image decoder module
 - [ ] Create http server to support printing via web
 - [ ] Create tool operator page to send commands to the http server
 - [ ] Support png and jpeg image types
 - [ ] Create label designer
 - [ ] Create support for other printer models

 