import random, time, pdb, sys
from yeelight import Bulb


bulb = Bulb("192.168.1.133")

GAME_COLORS = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255)}
DEFAULT_COLOR = (255, 255, 255)
INIT_NUM = 3
LARGE_DELAY = 1
SMALL_DELAY = 0.2

def chose_color():
	opt = None
	
	for i, c in enumerate(GAME_COLORS):
		print("%d) %s" % (i+1, c))
		
	while opt == None:
		try:
			opt = int(input("\n Next color: "))
		except:
			print("\nInvalid color")
			
	return GAME_COLORS.keys()[opt-1]
	
def choose_seq(n):
	seq = []
	for _ in range(n):
		seq.append(chose_color())
	return seq
	
def generate_seq(n):
	return [random.choice(GAME_COLORS.keys()) for _ in range(n)]
	
def show_seq(seq):
	bulb.turn_on()
	time.sleep(SMALL_DELAY)
	
	for c in seq:
		bulb.set_rgb(*GAME_COLORS[c])
		print(c, GAME_COLORS[c])
		time.sleep(LARGE_DELAY)
		bulb.set_rgb(*DEFAULT_COLOR)
		time.sleep(SMALL_DELAY)
		
	bulb.turn_off()


bulb.turn_on()
bulb.set_rgb(*DEFAULT_COLOR)
time.sleep(LARGE_DELAY)

seq = generate_seq(INIT_NUM)
print(seq)

while True:
	show_seq(seq)
	cseq = choose_seq(len(seq))
	print(cseq)
	if seq == cseq:
		print("Nice! Next round...")
		seq.append(random.choice(GAME_COLORS.keys()))
	else:
		print("Fail! :(")
		sys.exit(0)