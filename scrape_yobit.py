from yobit import *
from pbar import pbar

# import existing data
master = init_master(fetch_new=False)

# start scraping
while True:
    t0 = time.time()

    for i, pair in enumerate(master.keys()):
        pbar(start_time=t0, progress_pct=i/len(master.keys()))
        response = trades(pair, limit=2000)

        if len(response) == 0:
            break

        elif len(master[pair]) == 0:
            master[pair] = master[pair].append(response)

        else:
            new_data = response[response.index > master[pair].index[0]]
            if len(new_data) != 0:
                print('\nadding data to ' + pair + ', ' + str(len(new_data)) + ' new data point(s)')
                master[pair] = new_data.append(master[pair])

    print('\nsaving and starting another pass...')
    pickle.dump(master, open('master.pkl', 'wb'))

    # TODO: save to csv files, on a weekly basis
