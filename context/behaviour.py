
def transfer(amount:float, a:str, b:str, n_years:int, frequency:int) -> list:
    '''Create event rule for transfering funds from a->b every so and so'''

    event_list = list()
    for step in range(0,n_years*12+1):
        if step%frequency==0:
            event_list.append( {'step':step, 'from':a, 'to':b, 'amount':amount} )

    return(event_list)
