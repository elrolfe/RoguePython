from enum import Enum
import os

class Font(Enum):

    ATI_8X8 = {
    	'file': os.path.join('fonts', 'cp437-ATI-8x8.png'), 
    	'width': 8, 
    	'height': 8
    }

    ATI_8X14 = {
    	'file': os.path.join('fonts', 'cp437-ATI-8x14.png'), 
    	'width': 8, 
    	'height': 14
    }
    
    ATI_8X16 = {
    	'file': os.path.join('fonts', 'cp437-ATI-8x16.png'), 
    	'width': 8, 
    	'height': 16
    }
    
    ATI_10X10 = {
    	'file': os.path.join('fonts', 'cp437-ATI-10x10.png'), 
    	'width': 10, 
    	'height': 10
    }
    
    IBMCGA_8X8 = {
    	'file': os.path.join('fonts', 'cp437-IBM-CGA-8x8.png'), 
    	'width': 8, 
    	'height': 8
    }
    
    IBMCGA_10X10 = {
    	'file': os.path.join('fonts', 'cp437-IBM-CGA-10x10.png'), 
    	'width': 10, 
    	'height': 10
    }
    
    IBMCGA_12X12 = {
    	'file': os.path.join('fonts', 'cp437-IBM-CGA-12x12.png'), 
    	'width': 12, 
    	'height': 12
    }
    
    IBMEGA_8X14 = {
    	'file': os.path.join('fonts', 'cp437-IBM-EGA-8x14.png'), 
    	'width': 8, 
    	'height': 14
    }
    
    IBMVGA_8X16 = {
    	'file': os.path.join('fonts', 'cp437-IBM-VGA-8x16.png'), 
    	'width': 8, 
    	'height': 16
    }


