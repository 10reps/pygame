import pygame
import random
import time
from datetime import datetime

# 게임 초기화
pygame.init()


size = [400, 900]  # 게임 창 크기
screen = pygame.display.set_mode(size)

title = "My Game"  # 게임 제목
pygame.display.set_caption(title)

clock = pygame.time.Clock()  # 시계 만들기
###########################################################################################

# 플레이어 정보


class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, address):
        if address[-3:] == 'png':
            self.img = pygame.image.load(
                address).convert_alpha()  # 플레이어 이미지 불러오기
        else:
            self.img = pygame.image.load(address)

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))  # 플레이어 이미지 크기 변경
        self.sx, self.sy = self.img.get_size()  # self.img값(50, 50)을 가져와 sx값과 sy값을 정함

    def show(self):
        screen.blit(self.img, (self.x, self.y))


def crash(a, b):
    if (a.x-b.sx <= b.x) and (b.x <= a.x+a.sx):
        if (a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
    else:
        return False
###########################################################################################


ss = obj()  # obj클래스 불러와서 __init__ 함수 실행 됨

# 이미지 불러오는 함수
ss.put_img('C:/Developer/Python/pygame/playerShip3_red.png')

ss.change_size(50, 50)  # 플레이어 이미지 사이즈 변경 함수

# 플레이어 시작 위치 설정
ss.x = (size[0] / 2) - (ss.sx / 2)
ss.y = size[1] - ss.sy - 15

# 플레이어 움직임 설정
ss.move = 5
left_go = False
right_go = False
space_go = False

# 투사체
m_list = []
k = 0

# 적
a_list = []

# 카운트
kill = 0
loss = 0

# 게임종료
GO = 0
###########################################################################################

# 게임 대기 화면
SB = 0
while SB == 0:

    # FPS 설정
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1

    screen.fill((0, 0, 0))
    font = pygame.font.Font(
        'C:/Windows/Fonts/arialbi.ttf', 15)  # 폰트 불러온 후 사이즈 설정

    text = font.render(
        "PRESS SPACE KEY TO START THE GAME", True, (255, 255, 255))  # 문구 설정
    screen.blit(text, (40, round(size[1] / 2)))  # 화면에 텍스트 표시를 보여줌

    # 위에서 발생한 사건들을 업데이트 한다
    pygame.display.flip()
###########################################################################################

# 메인 이벤트
start_time = datetime.now()  # 이 코드가 실행되는 순간의 시간이 저장 됨
SB = 0
while SB == 0:

    # FPS 설정
    clock.tick(60)

    # 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 화면 위 모서리의 X버튼 누르면 게임 종료
            SB = 1

        if event.type == pygame.KEYDOWN:  # 어떤 키가 눌렸다면
            if event.key == pygame.K_LEFT:  # 왼쪽 키가 눌렸다면
                left_go = True

            elif event.key == pygame.K_RIGHT:  # 오른쪽 키가 눌렸다면
                right_go = True

            elif event.key == pygame.K_SPACE:  # 스페이스 바가 눌렸다면
                space_go = True
                k = 0

        if event.type == pygame.KEYUP:  # 어떤 키가 눌리지 않았다면
            if event.key == pygame.K_LEFT:  # 왼쪽 키가 눌리지 않았다면
                left_go = False

            elif event.key == pygame.K_RIGHT:  # 오른쪽 키가 눌리지 않았다면
                right_go = False

            elif event.key == pygame.K_SPACE:  # 스페이스 바가 눌리지 않았다면
                space_go = False

    # 시간 설정
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())  # 초 단위로 표기

    # 플레이어 움직임
    if left_go == True:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0

    elif right_go == True:
        ss.x += ss.move
        if ss.x > size[0] - ss.sx:
            ss.x = size[0] - ss.sx

###########################################################################################
    # 투사체 움직임
    if space_go == True and k % 6 == 0:
        mm = obj()  # obj클래스 불러와서 __init__ 함수 실행 됨

        # 이미지 불러오는 함수
        mm.put_img('C:/Developer/Python/pygame/laserRed02.png')

        mm.change_size(5, 15)  # 투사체 이미지 사이즈 변경 함수

        # 투사체 생성 위치 설정
        mm.x = round(ss.x + ss.sx / 2 - mm.sx / 2)
        mm.y = ss.y - mm.sy - 10

        mm.move = 15  # 투사체 이동속도

        m_list.append(mm)  # 투사체를 리스트 형식으로 담기

    k += 1
    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]  # m_list = m이기 때문에 m = mm이라고 봐도 됨 따라서 m.~ = mm.~ 이다
        m.y -= m.move

        if m.y <= -m.sy:
            d_list.append(i)  # d_list로 투사제 삽입

    for d in d_list:
        del m_list[d]  # d_list에 인자가 들어가면 투사체 삭제
###########################################################################################

    # 적 출현
    if random.random() > 0.98:
        aa = obj()  # obj클래스 불러와서 __init__ 함수 실행 됨

        # 이미지 불러오는 함수
        aa.put_img('C:/Developer/Python/pygame/enemyBlack1.png')

        aa.change_size(40, 40)  # 적 이미지 사이즈 변경 함수

        # 적 생성 위치 랜덤으로 설정
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx / 2))
        aa.y = 10

        aa.move = 1  # 적 이동속도

        a_list.append(aa)  # 적을 리스트 형식으로 담기

    d_list = []
    for i in range(len(a_list)):  # 적 아래로 조금씩 움직이기
        a = a_list[i]
        a.y += a.move

        if a.y >= size[1]:  # 적이 화면 아래 맨 끝에 닿으면 사라짐
            d_list.append(i)
            loss += 1  # 적을 놓치면 loss 카운트 1증가

    d_list.reverse()
    for d in d_list:
        del m_list[d]
###########################################################################################

    # 적 & 미사일 충돌판정
    dm_list = []
    da_list = []
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]

            if crash(m, a) == True:
                dm_list.append(i)
                da_list.append(j)

    dm_list = list(set(dm_list))  # 중복제거 후, 다시 리스트 자료형으로 변환
    da_list = list(set(da_list))

    dm_list.reverse()
    da_list.reverse()

    try:
        for dm in dm_list:  # 충돌하면 투사체를 화면에서 지움
            del m_list[dm]
        for da in da_list:  # 충돌하면 적을 화면에서 지움
            del a_list[da]
            kill += 1  # 적이 사라지면 kill 카운트 1증가

    except:
        pass

    for i in range(len(a_list)):
        a = a_list[i]

        if crash(a, ss) == True:
            SB = 1
            GO = 1
###########################################################################################

    screen.fill((0, 0, 0))
    ss.show()  # 플레이어 화면에 보이기

    for m in m_list:  # 투사체 회면에 보이기
        m.show()

    for a in a_list:  # 적 회면에 보이기
        a.show()

    font = pygame.font.Font(
        'C:/Windows/Fonts/arialbi.ttf', 20)  # 폰트 불러온 후 사이즈 설정

    # kill & loss 카운트 화면 표시
    text_kill = font.render("killed : {} loss : {}".format(
        kill, loss), True, (255, 255, 0))  # 문구 설정
    screen.blit(text_kill, (10, 5))  # 화면에 텍스트 표시를 보여줌

    # time 카운트 화면 표시
    text_time = font.render("Time : {}".format(
        delta_time), True, (255, 255, 255))  # 문구 설정
    screen.blit(text_time, (size[0] - 100, 5))  # 화면에 텍스트 표시를 보여줌

    # 위에서 발생한 사건들을 업데이트 한다
    pygame.display.flip()
###########################################################################################


# 게임 종료 화면
while GO == 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 화면 위 모서리의 X버튼 누르면 게임 종료
            GO = 0

    font = pygame.font.Font(
        'C:/Windows/Fonts/arialbi.ttf', 40)  # 폰트 불러온 후 사이즈 설정

    text = font.render(
        "GAME OVER", True, (255, 0, 0))  # 문구 설정
    screen.blit(text, (80, round(size[1] / 2 - 50)))  # 화면에 텍스트 표시를 보여줌

    # 위에서 발생한 사건들을 업데이트 한다
    pygame.display.flip()

# 게임 종료
pygame.quit()
