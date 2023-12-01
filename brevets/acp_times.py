"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders

Algorithm source: https://rusa.org/pages/acp-brevet-control-times-calculator
"""
import arrow


# redoing this completely since my project4 was a mess


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # using tables this time like slides suggested
    max_speeds = {
        (0, 200): 34.0, # first 200
        (200, 400): 32.0, # next 200
        (400, 600): 30.0, # next 200
        (600, 1000): 28.0, # next 400
        (1000, 1300): 26.0 } # next 400
    
    open_time = set_control_time(brevet_dist_km, control_dist_km, brevet_start_time, max_speeds, close=False)

    return open_time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    min_speeds = {
        (0, 600): 15.0,
        (600, 1000): 11.428,
        (1000, 1300): 13.333 }
    
    close_time = set_control_time(brevet_dist_km, control_dist_km, brevet_start_time, min_speeds, close=True)
    
    return close_time


def convert_time(hours):

    h = hours % 1 
    time = {"hours": hours // 1, # whole number of hours
            "minutes": round(h * 60) } # decimal hours to mins
    
    return time


def read_table(control_dist, speed_table):

    time_h = float(0) # using float hours and converting time to hours and mins at the end

    for control_range, speed in speed_table.items():
        low, high = control_range
        # closing controls less than 60km from the start are relaxed
        relaxed = 60 
        
        if control_dist >= relaxed:                                           
            if high == relaxed:
                continue
            elif low < relaxed:  
                low = 0     

        if control_dist >= high: # switch to next control range
            diff = high - low 
            time_h += diff / speed
        
        else:
            dist = control_dist - low
            time_h += dist / speed
            break

    return time_h


def set_control_time(brevet_dist, control_dist, start, table, close):

    if control_dist > brevet_dist * 1.2:
        raise ValueError(f"Control distance cannot be over 20% more than brevet distance.")# Control: {control_dist} Brevet: {brevet_dist}")

    if control_dist < brevet_dist:
        dist = control_dist
    else:
        dist = brevet_dist

    relaxed = 60 
    time = read_table(dist, table)
    # there is always at least an hour before close (relaxed)
    if (close is True) and (control_dist < relaxed): 
        time += 1  

    readable_time = convert_time(time)
    return start.shift(**readable_time)
