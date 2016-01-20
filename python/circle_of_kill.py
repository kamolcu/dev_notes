## This file depicts solution of a game:
## Rules:
## - There are n (> 1) people standing in circle shape and assign number 1 ... n
## - First person (No.1) will kill a person next to his left (No. 2)
## - Next alive person (No. 3) will kill a person next to his left (No. 4)
## - Repeat this loop until every alive one kill a person once, so end a killing round
## - Start new killing round with a person with least number assigned
## - Repeat until has only one alive and his number is the solution

import argparse
import sys

class People:
  def __init__(self, number=None, next=None, has_kill=False):
    self.has_kill = has_kill
    self.number = number
    self.next = next
  def __str__(self):
    return str(self.has_kill)

def prepare_circle(people_count):
    cc = []
    current = People(number=0)
    for ii in range(people_count):
        next = People(number=ii + 1)
        current.next = next
        cc.append(current)
        current = next
    cc[people_count - 1].next = cc[0]
    return cc

def has_end_round(circle):
    if(len(circle) == 1 and circle[0].has_kill == True):
        return True

    bool_list = map(lambda xx: xx.has_kill, circle)
    return reduce(lambda xx, yy: xx and yy , bool_list)

def has_end(circle):
    return has_end_round(circle) and len(circle) == 1

def reset_has_kill(circle):
    for person in circle:
        person.has_kill = False
    return circle

def prepare_message_input(start_person):
    return (start_person.number + 1, start_person.next.number + 1, start_person.next.next.number + 1)

def print_kill_summary(start_person, fill=3):
    (start_person, dead_person, next_person) = prepare_message_input(start_person)
    print 'Start person is %s, dead person is %s, next person is %s' % (str(start_person).rjust(fill), str(dead_person).rjust(fill), str(next_person).rjust(fill))

# =========
parser = argparse.ArgumentParser(description='Circle of kill')
parser.add_argument(
    'people_count',
    type=int,
    help='Start number of people, for example, 20, 100, etc.')
args = parser.parse_args()

if(args.people_count <= 1):
    msg = 'people_count must more than 1.'
    sys.exit(msg)

if(args.people_count > 5000):
    msg = 'people_count must less than 5000.'
    sys.exit(msg)


print 'Start finding solution with %s people ...' % str(args.people_count)
circle = prepare_circle(args.people_count)
round_count = 0
while(not has_end(circle)):
    circle = reset_has_kill(circle)
    start = circle[0]
    round_count += 1
    print 'Enter round %s' % round_count
    while True:
        print_kill_summary(start)
        start.has_kill = True
        circle.remove(start.next)
        start.next = start.next.next
        start = start.next
        if has_end_round(circle):
            print 'Number of people left = %s' % len(circle)
            print 'End round %s ...' % round_count
            break
print 'End of the game! Survival person is %s' % (circle[0].number + 1)
