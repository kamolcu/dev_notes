# -*- coding: utf-8 -*-
import argparse
def adjust(container_height, answer, blocks):
    counter = 0
    for item_list in answer:
        if item_list[1] == False:
            item_list[0] = container_height - blocks[counter]
            item_list[1] = True
        counter += 1
    return answer

def fill(pre_block, cur_block, next_block, prev_container_height):
    final = True
    # print('%s %s %s prev_container_height=%s' % (pre_block, cur_block, next_block, prev_container_height))
    wall_height = max(pre_block, prev_container_height)
    if (wall_height <= cur_block):
        return [[0, final]]
    if wall_height <= next_block and next_block >= prev_container_height:
        return [[wall_height - cur_block, final]]
    if pre_block < next_block:
        return [[min(prev_container_height, next_block), final]]
    final = False
    if cur_block >= next_block:
        return [[wall_height - cur_block, final]]
    else:
        return [[max(pre_block, prev_container_height), final]]

parser = argparse.ArgumentParser(description='Find water container size from block height array e.g. [0,1,1,4,0,3] - https://www.facebook.com/photo.php?fbid=10211777520625337&set=gm.717576955120243&type=3&theater')
parser.add_argument(
    'block',
    type=int,
    nargs='+',
    help='height of block in int'
)
args = parser.parse_args()

if __name__ == '__main__':
    answer = []
    # Put both ends with 0
    blocks = [0] + args.block + [0]
    global max_height, min_height
    max_height = max(args.block)
    min_height = min(args.block)
    prev_container_height = 0
    for index in range(1, len(blocks) - 1):
        fill_result = fill(pre_block=blocks[index-1], cur_block=blocks[index], next_block=blocks[index+1], prev_container_height=prev_container_height)
        # print(fill_result)
        answer = answer + fill_result
        if fill_result[0][0] > 0:
            prev_container_height = fill_result[0][0] + blocks[index]
        else:
            prev_container_height = 0
        if fill_result[0][1] == True:
            answer = adjust(container_height=prev_container_height, answer=answer, blocks=args.block)
    # print(answer)
    container_size = []
    for [item,flag] in answer:
        container_size = container_size + [item]
    print(container_size)
    print('container_size =', sum(container_size))
