from onepi.utils.simple_timer import SimpleTimer
import time

# these steps are necessary in order to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)


def test_start_time():
    count = 0

    def time_elapsed():
        count += my_timer.get_time()

    my_timer = SimpleTimer(increment=1, function=time_elapsed)
    my_timer.start()
    assert count == 0
    time.sleep(1.2)
    assert count == 1


def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")

    # def time_elapsed():
    #     print("...elapsed time:", my_timer.get_time())

    # my_timer = SimpleTimer(increment=1, function=time_elapsed)

    # my_timer.start()
    # time.sleep(5.4)

    # print("Starting timer 2nd time")
    # my_timer.start()
    # time.sleep(3)
    # print("Stopping timer")
    # my_timer.stop()
    # time.sleep(3)
    # print("Starting timer 3rd time")
    # my_timer.start()
    # time.sleep(3)
    # print("Stopping timer")
    # my_timer.stop()
    # time.sleep(3)
    # print("Reset and start timer 4th time")
    # my_timer.reset()
    # my_timer.start()
    # time.sleep(5.1)
    # print("Stopping timer")
    # my_timer.stop()
    # my_timer.reset()
    # time.sleep(3)
    # print("done")


if __name__ == "__main__":
    main()
