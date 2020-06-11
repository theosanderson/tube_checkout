import os
import atexit
import threading
import time
import subprocess
watcher_thread = None
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def _kill_ot_server():
    subprocess.check_output(
        "systemctl stop opentrons-robot-server", shell=True)


def temporarily_kill_ot_server():
    """ Kills the OpenTrons robot server service, and sets it to restart at exit. """
    _kill_ot_server()

    def restart_ot_server():
        subprocess.check_output(
            "systemctl start opentrons-robot-server", shell=True)
    atexit.register(restart_ot_server)


def set_button_as_kill_switch(protocol):
    global watcher_thread

    def button_watcher():
        while not threading.current_thread().stopped():
            time.sleep(0.1)
            if protocol._hw_manager.hardware._backend.gpio_chardev.read_button():
                protocol._hw_manager.hardware.halt()
    watcher_thread = StoppableThread(target=button_watcher)
    watcher_thread.start()

    def stop_watcher():
        watcher_thread.stop()
    atexit.register(stop_watcher)
    


class BiggerLabwareFromComponents:

    def __init__(self, grid):
        """ Order components from top left
        grid = [ [racks['4'], racks['5']],
                 [racks['1'] , racks['2']]
        """

        self.grid = grid
        self.y_dim = len(grid)
        if type(grid[0]) is not list:
            raise ValueError("""grid must be a grid.. like
                             
                         [
                             [ 4,5 ],
                             [ 1,2 ]
                                      ]""")
        self.x_dim = len(grid[0])
        big_columns = []
        for x in range(self.x_dim):
            temp_columns = None
            for y in range(self.y_dim):
                this_labware = grid[y][x]
                if not temp_columns:
                    temp_columns = this_labware.columns()
                else:
                    for i, col in enumerate(this_labware.columns()):
                        temp_columns[i].extend(this_labware.columns()[i])
            big_columns.extend(temp_columns)
        self.big_columns = big_columns

    def columns(self):
        return self.big_columns

    def rows(self):
        raise NotImplementedError("Only .columns() is available")
        
    def __getitem__(self, well):
        """Get well in A1, B3 form. """
        row_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        first_char = well[0]
        assert first_char in row_names
        row_index = row_names.find(first_char)
        col_index = int(well[1:]) - 1
        return self.columns()[col_index][row_index]
    def wells(self):
        output = []
        for col in self.columns():
            for well in col:
                output.append(well)
        return output
            
                     
