#w = 800  
#h = 600
#
#n = 13
#ncards = 4*n
#card_w = 72
#card_h = 100
#
#path = 'images/800x600/classic/'
#suits = ['P', 'D', 'C', 'T']
#hidden_card_filename = 'images/800x600/hidden.png'

def init(screen_size=(800, 600)):
    global w, h, card_w, card_h, n, ncards, path, suits, hidden_card_filename
    if screen_size == (640, 480):
        w = 640
        h = 480
        card_w = 43
        card_h = 64 
        path = "images/640x480/"
        hidden_card_filename = 'images/640x480/hidden.gif'
        suits = ['c', 'd', 'h', 's']
        n = 13
        ncards = 4*n
    elif screen_size == (800, 600):
        w = 800
        h = 600
        card_w = 57
        card_h = 85
        path = "images/800x600/"
        hidden_card_filename = 'images/800x600/hidden.gif'
        suits = ['c', 'd', 'h', 's']
        n = 13
        ncards = 4*n

#        else:
#            card_w = 66
#            card_h = 90
#            path = "images/800x600/"
#            hidden_card_filename = 'images/800x600/hidden.png'
    elif screen_size == (1024, 768):
        w = 1024 
        h = 768
        card_w = 79
        card_h = 123
        path = "images/1024x768/"
        hidden_card_filename = 'images/1024x768/hidden.gif'
        suits = ['c', 'd', 'h', 's']
        n = 13
        ncards = 4*n
#    else:
#        path = path + "spain/"
#        suits = ['B', 'C', 'O', 'E']
#        n = 12
#        ncards = 4*n
    



