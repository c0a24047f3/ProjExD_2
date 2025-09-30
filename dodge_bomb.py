import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5), pg.K_DOWN:(0,+5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(+5,0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct :pg.Rect) ->tuple[bool, bool]: #爆弾が当たっている判定
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
    if rct.top < 0 or HEIGHT < rct.bottom:#縦にはみ出ていたらif
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    """

    引数:
        screen (pg.Surface): 画面(screen)
    """
    game_img = pg.Surface((1100, 650)) #空のサーフェス
    pg.draw.rect(game_img, (0, 0, 0), (0, 0, 1100, 650))# 黒い四角形を作成
    game_img.set_alpha(255) #黒画面の透明度
    fonto = pg.font.Font(None, 80)#フォントを作成
    img_cry = pg.image.load("fig/8.png")#画像を持ってくる
    txt = fonto.render("Game Over", True, (255, 255, 255))
    game_img.blit(txt, [400, 300])#文字
    game_img.blit(img_cry, [355, 300])#左のこうかとん
    game_img.blit(img_cry, [710,300])#右のこうかとん
    screen.blit(game_img,[0, 0])  
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:# 爆弾を拡大と加速
    """

    Returns:
        tuple[list[pg.Surface], list[int]]: 拡大と加速のタプル
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0)) #黒い枠をなくす
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:#こうかとんの移動方向へ向く
    """

    Returns:
        dict[tuple[int, int], pg.Surface]: 移動方向の辞書
    """
    kk_img = pg.image.load("fig/3.png")
    rotozoom = pg.transform.rotozoom
    kk_dict = {
    ( 0, 0): rotozoom(kk_img, 0, 1.0), # キー押下がない場合
    (+5, 0): rotozoom(kk_img, 180, 1.0), # 右
    (+5,-5): rotozoom(kk_img, 135, 1.0), # 右上
    ( 0,-5): rotozoom(kk_img, 90, 1.0), # 上
    ( -5, -5): rotozoom(kk_img, 315, 1.0), # 左上
    (-5, 0): rotozoom(kk_img, 0, 1.0), # 左
    (-5,+5): rotozoom(kk_img, 45, 1.0), # 左下
    ( 0,+5): rotozoom(kk_img, 270, 1.0), # 下 
    (+5,+5): rotozoom(kk_img, 45, 1.0) # 右下
    }
    return kk_dict

def semaku() -> tuple[list[int]]:
    screen_dec = [a for a in range(1, 10)]
    return screen_dec

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) #空のサーフェス
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10) #爆弾イメージ　赤い円
    bb_img.set_colorkey((0,0,0)) #黒い枠をなくす
    bb_rct = bb_img.get_rect() 
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #爆弾の座標　画面がずれてもWIDTHとHEIGHTを使用することで画面外に出ない
    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs,bb_accs = init_bb_imgs()
    screen_dec = semaku
    kk_imgs = get_kk_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):# こうかとんと爆弾の衝突の判定
            gameover(screen)
            return

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
        kk_img = kk_imgs[tuple(sum_mv)]
        if sum_mv == [+5, 0] or sum_mv == [+5, -5] or sum_mv == [0, -5] or sum_mv == [0, +5]:
            kk_img = pg.transform.flip(kk_img, False, True)
        elif sum_mv == [+5, +5]:
            kk_img = pg.transform.flip(kk_img, True, False)
        if check_bound(kk_rct) != (True,True):#こうかとんがはみ出ているとき
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko,tate = check_bound(bb_rct)
        if not yoko:#横方向にはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
        avx = vx*bb_accs[min(tmr//500, 9)] #爆弾のx軸の加速
        avy = vy*bb_accs[min(tmr//500, 9)] #y軸の加速
        bb_rct.move_ip(avx,avy) #爆弾を動かす
        bb_img = bb_imgs[min(tmr//500, 9)]#大きさ
        """WIDTH_af = WIDTH*screen_dec[9-tmr//500]/10
        HEIGHT_af = HEIGHT*screen_dec[9-tmr//500]/10
        screen = pg.display.set_mode((WIDTH_af, HEIGHT_af))"""#途中
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
