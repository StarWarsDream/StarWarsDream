           # 绘制全屏炸弹数量
            bomb_text=bomb_font.render("× %d" % bomb_num,True,WHITE)
            text_rect=bomb_text.get_rect()
            screen.blit(bomb_image,(10,height-10-bomb_rect.height))
            screen.blit(bomb_text,(20+bomb_rect.width,height-5-bomb_rect.height))

            #绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,\
                                (width-10-(i+1)*life_rect.width,\
                                 height-10-life_rect.height))
            score_text=score_font.render("Score : %s"% str(score),True,WHITE)
            screen.blit(score_text,(10,5))

        #绘制游戏结束画面
        elif life_num==0:
            #背景音乐停止
            pygame.mixer.music.stop()
            #音效停止
            pygame.mixer.stop()
            #补给包计时器停止
            pygame.time.set_timer(SUPPLY_TIME,0)
            #读取历史最高得分
            if not recorded:
                recorded=True
                with open("record.txt","r") as f:
                    record_score=int(f.read())
                #如果分数高于历史最高成绩，存入成绩
                if score>record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
            #绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()      
        

        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)

        #----------切换图片----------------
        if not(delay%5):
            switch_image=not switch_image

        delay-=1
        if not delay:
            delay=100
         #----------切换图片----------------

        pygame.display.flip()

        clock.tick(60)


if __name__=="__main__":
    try:
        main()
    except SystemExit:   #正常退出
        pass
    except:  #其他异常
        traceback.print_exc()
        pygame.quit()
        input()
