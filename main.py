import random

TOLL = 500  # 통행료
BUY = 300   # 도시 구입료
TURN = 30   # 턴 기본 실행 횟수

class City:
    def __init__(self, name):
        self.name = name
        self.owner = 0

    def stat(self):
        if self.owner == 0:
            print("(주인 없음)")
        else:
            print("(플레이어 %d의 소유)" %self.owner)

class Player:
    def __init__(self, num):
        self.balance = 4000
        self.loc = 0
        self.p_num = num

    def move(self, dice):
        self.loc = (self.loc + dice) % 10

    # 해당 도시의 class를 매개변수로 사용한다.
    def buy(self, City):
        self.balance -= BUY
        City.owner = self.p_num

    # 상태 플레이어 class를 매개변수로 사용한다.
    def toll(self, Player):
        self.balance -= TOLL
        Player.balance += TOLL

city = [City("START"), City("Seoul"), City("Tokyo"), City("Sydney"), City("LA"), City("Paris"),
        City("Hanoi"), City("New Delhi"), City("Phuket"), City("Cairo")]

p = [Player(1), Player(2)]

def display(st,end,dir):
    for i in range(st,end,dir):
        # 첫번째 줄) 각 도시의 간격은 space * 4. 직사각형의 길이는 16.
        print("{:^20}".format("┌──────────────┐"), end = '')
    print("\n", end = '')

    # 두번째 줄) 도시 이름 및 소유주 출력
    for i in range(st,end,dir):
        print("  │", end='')
        # 해당 포매팅의 글자수(도시명의 길이)가 매번 달라지기 때문에 단일 명령으로 처리할 수 없다.
        # city의 주인이 있으면 도시명과 주인을 출력한다.
        if city[i].owner != 0:
            if len((city[i]).name) == 2: # LA
                print("{:^15}".format("%s(%d)") %((city[i]).name, city[i].owner), end = '')
            elif len((city[i]).name) == 5: # Start,Seoul,Tokyo,Cairo,Hanoi,Paris
                print("{:^12}".format("%s(%d)") % ((city[i]).name, city[i].owner), end='')
            elif len((city[i]).name) == 6: # Sydney, Phuket
                print("{:^11}".format("%s(%d)") % ((city[i]).name, city[i].owner), end='')
            else: # New Delhi
                print("{:^8}".format("%s(%d)") % ((city[i]).name, city[i].owner), end='')

        # city의 주인이 없으면 도시명만 출력한다.
        else:
            if len((city[i]).name) == 2: # LA
                print("{:^14}".format("%s") % (city[i]).name, end='')
            elif len((city[i]).name) == 5: # START,Seoul,Tokyo,Cairo,Hanoi,Paris
                print("{:^11}".format("%s") % (city[i]).name, end='')
            elif len((city[i]).name) == 6: # Sydney,Phuket
                print("{:^10}".format("%s") % (city[i]).name, end='')
            else: # New Delhi
                print("{:^7}".format("%s") % (city[i]).name, end='')
        print("│  ", end='')
    print("\n", end = '')

    # 세번째 줄) 해당 도시에 도착한 플레이어를 표시한다.
    for i in range(st,end,dir):
        print("  │", end='')
        if (p[0].loc == i) and (p[1].loc == i):
            print("{:^14}".format("(1) (2)"), end='')
        elif p[0].loc == i:
            print("{:^14}".format("(1)"), end='')
        elif p[1].loc == i:
            print("{:^14}".format("(2)"), end='')
        else:
            print(" " * 14, end='')
        print("│  ", end='')
    print("\n", end = '')

    # 네번째 줄)
    for i in range(st,end,dir):
        print("{:^20}".format("└──────────────┘"), end = '')

# TURN은 최대 'TURN'번 반복한다.
for i in range(1,TURN + 1):
    game_keeper = 1         # 게임의 흐름을 결정하는 변수(파산한 플레이어 존재 확인)
    print("\n--------------------------------")
    print("TURN %d\n" %i)

    # P1, P2가 한 번씩 움직이는 것이 한 턴이다.
    for j in range(0,2):
        dice = random.randrange(1,7)
        p[j].move(dice)

        # MAP display(시작 숫자, 끝 숫자, 방향 결정)
        display(0,5,1)
        print("\n         ↑", " " * 78, "↓")
        display(9,4,-1)
        print("\n")

        # 각 Player가 거치는 과정
        print("%d번 플레이어의 주사위: %d" %(j+1, dice))
        print("%s에 도착" %city[p[j].loc].name, end = '')
        # 도착한 곳이 START가 아닐 경우에만 정상적인 과정을 거친다.
        if p[j].loc != 0:
            city[p[j].loc].stat()

            # CASE 1: 도착한 곳이 빈 땅일 때
            if city[p[j].loc].owner == 0:
                # 1)돈이 충분한 경우
                if p[j].balance >= BUY:
                    p[j].buy(city[p[j].loc])
                    print("%d번 플레이어는 %s를 구입합니다." %(j+1, city[p[j].loc].name))
                # 2)돈이 부족한 경우
                else:
                    print("잔고가 부족하여 구입할 수 없습니다.")

            # CASE 2: 도착한 곳이 내 땅일 때 (아무것도 하지 않음)
            elif city[p[j].loc].owner == p[j].p_num:
                pass

            # CASE 3: 도착한 곳이 남의 땅일 때
            else:
                # 1)돈이 충분한 경우 ('~'는 비트연산자로, ~1 == 0이다. 즉 p[~j]는 상대 플레이어)
                if p[j].balance >= TOLL:
                    p[j].toll(p[~j])
                    print("%d번 플레이어는 통행료를 지불합니다." %(j+1))
                # 2)돈이 부족한 경우 플레이어의 행동 즉시 종료
                else:
                    game_keeper = 0
                    print("돈이 부족합니다. %d번 플레이어가 파산하였습니다." %(j+1))
                    break
        # START에 도착한 경우
        else:
            print("\n", end ='')
        # 각 플레이어의 턴이 끝나면 잔고를 출력한다(파산한 경우 제외)
        print("%d번 플레이어의 잔고는 %d\n" % (j+1, p[j].balance))

    # 게임 종료(Turn 반복문 종료)
    if game_keeper == 0:
        break
    else:
        # pause는 Turn별로 볼 수 있도록 만드는 임시변수로, 게임 내에서는 사용하지 않는다.
        pause = input("진행하시려면 Enter키를 눌러주세요...")

# 승패가 결정되지 않고 종료되면 해당 상황에 대한 설명을 추가로 출력한다.
print("\n\n  게  임  종  료", end = '')
if game_keeper == 1:
    print(" (%d회 동안 승패가 결정나지 않음)" %TURN)