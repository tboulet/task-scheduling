from datetime import datetime

def n2letter(n):
    '''0 to 'a', 1 to 'b', ... '''
    return chr(96+n)
    
def string2duration(string):
    ''' "01:50:19.3177493" to duration in seconds'''
    date =  datetime.strptime(string.split('.')[0], "%H:%M:%S")
    return date.second + 60*date.minute + 3600*date.hour