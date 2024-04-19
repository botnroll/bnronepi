from onepi.utils.simple_timer import SimpleTimer

import os
import sys
import time

# these steps are necessary in order to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

def time_elapsed():
    pass

def test_start_time():
    my_timer = SimpleTimer(increment=1, function=time_elapsed)
    my_timer.start()
    assert my_timer.get_time() == 0
    time.sleep(1.2)
    assert my_timer.get_time() == 1
    my_timer.stop()

def test_stop_time():
    my_timer = SimpleTimer(increment=1, function=time_elapsed)
    my_timer.start()
    assert my_timer.get_time() == 0
    time.sleep(1.2)
    my_timer.stop()
    assert my_timer.get_time() == 1
    time.sleep(1.2)
    assert my_timer.get_time() == 1
    my_timer.start()
    time.sleep(1.2)
    assert my_timer.get_time() == 2
    my_timer.stop()
    
def test_reset_time():
    my_timer = SimpleTimer(increment=1, function=time_elapsed)
    my_timer.start()
    assert my_timer.get_time() == 0
    time.sleep(1.2)
    my_timer.reset()
    assert my_timer.get_time() == 0
    time.sleep(1.2)
    assert my_timer.get_time() == 0
    my_timer.start()
    time.sleep(1.2)
    assert my_timer.get_time() == 1
    my_timer.stop()
    
def main():
    print("Run tests using: pytest", os.path.basename(__file__), "-s")

if __name__ == "__main__":
    main()
