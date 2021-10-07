import os

def track(message):
    '''
    Objective:
        - Write what the file is doing
    Input:
        - Message: Message that has to be written to the track file
    Output: 
        - None
    ''' 
    path = '../reports/tracking'
    file = path+'/track.txt'

    # Directory creation if doesn't exists 
    try:
        os.makedirs(path)
    except OSError:
        pass
    
    # Open the file in append & read mode ('a+')
    with open(file, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read()
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(message)