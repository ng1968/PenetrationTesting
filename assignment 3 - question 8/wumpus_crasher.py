""" Hunt the Wumpus Crasher. """

from subprocess import Popen, PIPE, STDOUT


def main(): 
  buf = 'a'  # Buffer variable.
  seg_fault = False  # Keeps track if we found segmentaion fault.
  
  # Loop that will continue to increase the size of the buffer
  # until the segmentation fault happens.
  while not seg_fault:
    # Passes a string to  the wumpus program
    wump = Popen(f'echo "{buf}" | ./wumpus', universal_newlines=True,
                 stdout=PIPE, stderr=STDOUT, shell=True)
    # Loops through the output.
    for x in iter(wump.stdout.readline, ''):
      if 'Segmentation fault' in x:  # Segmentation fault found.
        print(x.strip())
        print('The programs breaks after {0:d} bytes'.format(len(buf)+1))
        seg_fault = True
        break
      # The last line of the output is usually 'Move or shoot?'
      # therefore we break and kill out the proccess and start again
      # with a bigger buffer
      if 'Move' in x:
        print(x.strip())
        buf += 'a'
        break
    wump.kill()


if __name__ == '__main__':
  main()
