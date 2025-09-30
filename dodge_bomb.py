import os
import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5), pg.K_DOWN:(0,+5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(+5,0)}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct :pg.Rect) ->tuple[bool, bool]:
    """

    引数:
        rct (pg.Rect): こうかとんRectか爆弾Rect

    戻り値:
        tuple[bool, bool]: タプル(横が出ているかの判定結果, 縦が出ているかの判定結果)(画面内ならTrue)
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right: #横にはみ出ていたらのif
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) #空のサーフェス
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10) #爆弾イメージ　赤い円
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect() #黒い枠をなくす
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #爆弾の座標　画面がずれてもWIDTHとHEIGHTを使用することで画面外に出ない
    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,my in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += my[0]
                sum_mv[1] += my[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):#こうかとんがはみ出ているとき
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko,tate = check_bound(bb_rct)
        if not yoko:#横方向にはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -2
        bb_rct.move_ip(vx,vy) #爆弾を動かす
        screen.blit(bb_img, bb_rct)  
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
