#!/usr/bin/env python3
import dice_game
from dice_game import ParityError
import curses
from curses import wrapper


start_pos = None
end_pos = None
start_rot = None
end_rot = None
cursor_pos = (1,1)

def draw_grid(stdscr):
    """
    Clears and draws the main grid.
    """
    for i in range(dice_game.GRID_SIZE):
        for j in range(dice_game.GRID_SIZE):
            stdscr.addstr(j*4,i*6,'+-----+')
            for k in range(1,4):
                stdscr.addstr(j*4+k, i*6, '|     |')

        stdscr.addstr(dice_game.GRID_SIZE*4,i*6,'+-----+')

def draw_commands(stdscr):
    x = dice_game.GRID_SIZE * 6 + 4
    stdscr.addstr(1, x, "Commands:")
    stdscr.addstr(2, x, "s  Set start")
    stdscr.addstr(3, x, "e  Set end")
    stdscr.addstr(4, x, "g  Set grid size")
    stdscr.addstr(5, x, "b  Toggle blocked")
    stdscr.addstr(6, x, "c  Toggle chirality")
    stdscr.addstr(7, x, "1-6  Set dice face")
    stdscr.addstr(8, x, "r  Rotate dice")
    stdscr.addstr(9, x, "arrows   Move")
    stdscr.addstr(10, x, "space    Solve")
    stdscr.addstr(11, x, "q  Quit")

def process_commands(stdscr, key):
    global start_pos
    global end_pos
    global start_rot
    global end_rot
    global cursor_pos

    filled_pos = {start_pos, end_pos}.union(dice_game.blocked_squares)
    empty_sq = cursor_pos not in filled_pos

    stdscr.addstr(15,dice_game.GRID_SIZE * 6 + 4,' '*10)
    stdscr.addstr(15,dice_game.GRID_SIZE * 6 + 4,key)
    
    if key == 's':
        if empty_sq:
            start_pos = cursor_pos

            if start_rot is None:
                start_rot = dice_game.get_dice_orientation_front(1)

    elif key == 'e':
        if empty_sq:
            end_pos = cursor_pos
            
            if end_rot is None:
                end_rot = dice_game.get_dice_orientation_front(1)

    elif key == 'g':
        size = stdscr.getkey()
        try:
            dice_game.GRID_SIZE = max(int(size),1)
            start_pos = None
            end_pos = None
            start_rot = None
            end_rot = None
            cursor_pos = (1,1)
            dice_game.blocked_squares = set()

            stdscr.clear()
            draw_grid(stdscr)
            draw_commands(stdscr)
        except ValueError:
            pass

    elif key == 'b':
        if cursor_pos in dice_game.blocked_squares:
            dice_game.blocked_squares.remove(cursor_pos)

        elif empty_sq:
            dice_game.blocked_squares.add(cursor_pos)

    elif key == 'c':
        if dice_game.DICE is dice_game.LEFT_HANDED_DICE:
            dice_game.DICE = dice_game.RIGHT_HANDED_DICE

        else:
            dice_game.DICE = dice_game.LEFT_HANDED_DICE

    elif key in (str(i) for i in range(1,7)):
        rot = dice_game.get_dice_orientation_front(int(key))

        if cursor_pos == start_pos:
            start_rot = rot

        elif cursor_pos == end_pos:
            end_rot = rot

    elif key == 'r':
        if cursor_pos == start_pos:
            start_rot = dice_game.ROTATION_CLOCKWISE @ start_rot
        
        elif cursor_pos == end_pos:
            end_rot = dice_game.ROTATION_CLOCKWISE @ end_rot

    elif key == 'KEY_UP':
        cursor_pos = (cursor_pos[0], min(dice_game.GRID_SIZE, cursor_pos[1]+1))

    elif key == 'KEY_DOWN':
        cursor_pos = (cursor_pos[0], max(1, cursor_pos[1]-1))

    elif key == 'KEY_RIGHT':
        cursor_pos = (min(dice_game.GRID_SIZE, cursor_pos[0]+1), cursor_pos[1])

    elif key == 'KEY_LEFT':
        cursor_pos = (max(1, cursor_pos[0]-1), cursor_pos[1])

    elif key == ' ':
        if ((start_pos is not None) and (start_rot is not None) 
            and (end_pos is not None) and (end_rot is not None)):

            try:
                solutions = dice_game.generate_solution_paths(
                        start_pos, end_pos, start_rot, end_rot)
            except ParityError as e:
                solutions = e.args

            draw_solutions(stdscr, solutions, 20)

    elif key == 'q':
        return False

    return True


def draw_solutions(stdscr, solutions, maximum):
    x = dice_game.GRID_SIZE * 6 + 30
    stdscr.addstr(1, x, "Solutions:")

    for i in range(maximum+1):
        stdscr.addstr(2+i, x, ' '*20)

    for i,s in enumerate(solutions):
        stdscr.addstr(2+i, x, s)
        if i == maximum:
            break

def grid_center(pos):
    """
    Goes from (x,y) grid position to curses screen position.
    """
    x0 = -3
    y0 = dice_game.GRID_SIZE * 4 + 2

    x = x0 + pos[0] * 6
    y = y0 - pos[1] * 4

    return x,y

def draw_dice(stdscr, pos, rot):
    x,y = grid_center(pos)

    stdscr.addch(y,x,   str(dice_game.get_dice_face(rot, (0,0,1))))
    stdscr.addch(y-1,x, str(dice_game.get_dice_face(rot, (0,1,0))))
    stdscr.addch(y+1,x, str(dice_game.get_dice_face(rot, (0,-1,0))))
    stdscr.addch(y,x-2, str(dice_game.get_dice_face(rot, (-1,0,0))))
    stdscr.addch(y,x+2, str(dice_game.get_dice_face(rot, (1,0,0))))

def update(stdscr):
    draw_grid(stdscr)

    if start_pos is not None:
        x,y = grid_center(start_pos)
        stdscr.addch(y-1,x-2, 's')

        if start_rot is not None:
            draw_dice(stdscr, start_pos, start_rot)

    if end_pos is not None:
        x,y = grid_center(end_pos)
        stdscr.addch(y-1,x-2, 'e')

        if end_rot is not None:
            draw_dice(stdscr, end_pos, end_rot)

    for square in dice_game.blocked_squares:
        stdscr.addch(*(grid_center(square)[::-1]), 'b')

    stdscr.move(*(grid_center(cursor_pos)[::-1]))

def main(stdscr):
    stdscr.clear()

    draw_commands(stdscr)

    update(stdscr)
    stdscr.refresh()
    
    while process_commands(stdscr, stdscr.getkey()):
        update(stdscr)
        stdscr.refresh()

wrapper(main)
