from yobit import *
import sys

# import existing data
master = init_master(fetch_new=False)

# start scraping
while True:

    for i, pair in enumerate(master.keys()):
        response = trades(pair, limit=2000)

        if len(response) == 0:
            continue

        elif len(master[pair]) == 0:
            master[pair] = master[pair].append(response)

        else:
            new_data = response[response.index > master[pair].index[0]]
            if len(new_data) != 0:
                print('adding data to ' + pair + ', ' + str(len(new_data)) + ' new data point(s)')
                sys.stdout.flush() # forces to write when running in background
                master[pair] = new_data.append(master[pair])

    print('saving and starting another pass...')
    sys.stdout.flush() # forces to write when running in background
    pickle.dump(master, open('master.pkl', 'wb'))

    # TODO: save to csv files, on a weekly basis
