# To use:
# from pbar import pbar # my custom progress bar
import math
import time

def pbar(progress_pct, start_time):

    # TODO: implement Kalman filter for remaining_sec prediction

    elapsed_sec = time.time() - start_time
    if progress_pct != 0.0:
        remaining_sec = (elapsed_sec / progress_pct) - elapsed_sec

    else:
        remaining_sec = 100

    progress_pct_str = '{:3.1f}%'.format(100 * progress_pct)
    elapsed_time_str = 'elapsed: ' + sec2str(elapsed_sec)
    remaining_time_str = 'remaining: ' + sec2str(remaining_sec)

    output_str = progress_pct_str + '\t\t'
    output_str += elapsed_time_str + '\t\t'
    output_str += remaining_time_str + '\t\t'
    print(output_str, end='\r')

def sec2str(remaining_sec):
    seconds = math.floor(remaining_sec % 60 % 60)
    minutes = math.floor(remaining_sec / 60 % 60)
    hours   = math.floor(remaining_sec / 60 / 60)
    string = '{:2}:{:2}:{:2}'.format(hours, minutes, seconds)
    return string
