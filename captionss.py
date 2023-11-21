import sys
import time

def main(mark_array, response):
    count = 0
    current = 0
    for i in range(len(response.timepoints)):
        count += 1
        current += 1
        with open("output.txt", "a", encoding="utf-8") as out:
            out.write(mark_array[int(response.timepoints[i].mark_name)] + " ")
        if i != len(response.timepoints) - 1:
            total_time = response.timepoints[i + 1].time_seconds
            time.sleep(total_time - response.timepoints[i].time_seconds)
        if current == 25:
                open('output.txt', 'w', encoding="utf-8").close()
                current = 0
                count = 0
        elif count % 7 == 0:
            with open("output.txt", "a", encoding="utf-8") as out:
                out.write("\n")
    time.sleep(2)
    open('output.txt', 'w').close()


if __name__ == "__main__":
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    main(arg1, arg2)





    