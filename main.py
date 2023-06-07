from Student_controller import StudentManager, StudentGUI
import os
#os.environ['TK_SILENCE_DEPRECATION'] = '1'

if __name__ == '__main__':
    manager = StudentManager()
    # Create the GUI
    gui = StudentGUI(manager)
    