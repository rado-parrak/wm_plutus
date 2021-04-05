def update_events(events:dict, new_events:dict) -> dict:
    for k in new_events.keys():
        if k in events.keys():
            events[k].extend(new_events[k])
        else:
            events[k] = new_events[k]
            
    return(events)

def buy_real_estate_on_mortgage(step:int, 
                                mortgage_principal:float, 
                                mortgage_cnit:float, 
                                mortgage_maturity:int,
                                real_estate_value:float,
                                real_estate_property_tax:float,
                                house_community_costs:float,
                                real_estate_index_name:str,
                                events:dict) -> dict:
    ''' Mortgage is gotten in step, Real-estate is bought in step+1'''
    
    # (i) mortage event
    mortgage_event = dict()
    mortgage_event['step'] = step
    mortgage_event['type'] = "Mortgage"
    mortgage_event['id'] = 'mortgage_taken_in_step_'+str(step)
    mortgage_event['principal'] = mortgage_principal
    mortgage_event['cnit'] = mortgage_cnit
    mortgage_event['maturity_in_years'] = mortgage_maturity
    mortgage_event['current_step'] = step

    # (ii) real-estate event
    real_estate_event = dict()
    real_estate_event['step'] = step+1
    real_estate_event['type'] = 'RealEstate'
    real_estate_event['id'] = 'real_estate_bought_with_mortgage_from_step_'+str(step)
    real_estate_event['current_market_value'] = real_estate_value
    real_estate_event['property_tax'] = real_estate_property_tax
    real_estate_event['house_community_costs'] = house_community_costs
    real_estate_event['real_estate_index'] = real_estate_index_name
    real_estate_event['events'] = events
    real_estate_event['current_step'] = step+1

    # compose into event dict
    new_events = {'buy':[real_estate_event], 'create':[mortgage_event]}

    return(new_events)

