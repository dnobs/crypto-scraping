from yobit import *
from pbar import pbar

# import existing data
master = init_master()

# start scraping
while True:
    i = 0
    t0 = time.time()
    for pair in master.keys():
        i += 1
        pbar(start_time=t0, progress_pct=i/len(pairs))

        # Look for new info, structed as a "do-while" loop
        request_limit = 200
        new_data = []
        while True:

            response = trades(pair, limit=request_limit)
            if len(response) == 0:
                break

            if len(master[pair]) == 0:
                master[pair] = master[pair].append(response)
            else:
                new_data = response[response.index > master[pair].index[0]]
                if len(new_data) != 0:
                    print('\nadding data to ' + pair + ', ' + str(len(new_data)) + ' new data point(s)')
                    master[pair] = new_data.append(master[pair])

            if request_limit >= 2000:
                break
            request_limit = 2000

    print('\nsaving and starting another pass...')
    pickle.dump(master, open('master.pkl', 'wb'))

# TODO: save to file
