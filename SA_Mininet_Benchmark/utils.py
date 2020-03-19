
def calculate_log_timestamps():
    f = open("log_times.txt", "r")

    lines = f.readlines()
    idx = 0
    time_start = 0

    for line in lines:

        line_idx = line.find('time')
        time_str = line[line_idx + 5:]

        # Even lines are transmitting
        if (idx % 2) == 0:
            time_start = float(time_str)
            print("T: " + line)
        else: # odd lines are recv
            print("R: " + line)
            print("Difference (seconds): " + str(float(time_str) - time_start))

        idx += 1


calculate_log_timestamps()
