import Image
import constants 


class LabelGrid():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
     
    def create_grid_img(self,label_img_file, x_count, x_gap):
        src = Image.open(label_img_file, 'r')        
        src_width,src_height = list(src.size)
        
        x_count = int(x_count)
        x_gap = float(x_gap)*constants.DOTS_PER_MM
        y_count=1
        y_gap=2*constants.DOTS_PER_MM
        
        new_width = int((src_width*x_count)+(x_gap*(x_count-1)))
        new_height = int((src_height*y_count)+(y_gap*(y_count-1)))
        
        new_img = Image.new("L",(new_width,new_height))
        
        x=0
        y=0
        for j in range(y_count) :
            for i in range(x_count):
#                 print((x,y))
                new_img.paste(src, (x,y))
                x+=int(src_width+x_gap)
            y+=int(src_height+y_gap)
            x=0
#         new_img.show()
        return new_img