def parse_data(data):
    data = data.split('?')
    
    method, action = data[0].split()

    if len(data) > 1:
        kwargs = dict([n.split('=') for n in data[1].split('&')])
    else:
        kwargs = {}
    
    return {'method':method, 'action': action, 'kwargs':kwargs}