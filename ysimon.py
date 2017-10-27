import random, time, pdb, sys
from yeelight import *

bulb = Bulb("192.168.1.133")

GAME_COLORS = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255)}
DEFAULT_COLOR = (255, 255, 255)
INIT_NUM = 3
LARGE_DELAY = 1000
SMALL_DELAY = 100

def chose_color():
	opt = None
	print("\nNext color:")
	for i, c in enumerate(GAME_COLORS):
		print("%d) %s" % (i+1, c))
		
	while opt == None:
		try:
			opt = int(input("\n >>> "))
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
	def start_flow(trans):
		bulb.start_flow(Flow(count = 1, transitions = trans))
		time.sleep((len(trans)/2)*(LARGE_DELAY+SMALL_DELAY) / 1000.0)
		
	bulb.turn_on()
	time.sleep(SMALL_DELAY / 1000.0)
	trans = []
	
	for c in seq:
		trans.append(RGBTransition(*GAME_COLORS[c], duration = LARGE_DELAY))
		trans.append(RGBTransition(*DEFAULT_COLOR, duration = SMALL_DELAY))
		
		if trans >= 8:
			start_flow(trans)
			trans = []
	
	if len(trans) > 0:
		start_flow(trans)


bulb.turn_on()
bulb.set_rgb(*DEFAULT_COLOR)
time.sleep(LARGE_DELAY / 1000.0)

seq = generate_seq(INIT_NUM)

while True:
	show_seq(seq)
	cseq = choose_seq(len(seq))

	if seq == cseq:
		print("Nice! Next round...")
		seq.append(random.choice(GAME_COLORS.keys()))
	else:
		print("Fail! It was: %s" % ", ".join(seq))
		sys.exit(0)