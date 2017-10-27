import random, time, pdb, sys
from yeelight import *

def choose_color(game):
	opt = None
	print("\nNext color:")
	for i, c in enumerate(game["colors"]):
		print("%d) %s" % (i+1, c))
		
	while opt == None:
		try:
			opt = int(input("\n>>> "))
		except:
			print("\nInvalid color")
			
	return game["colors"].keys()[opt-1]

def choose_seq(game, n):
	seq = []
	for _ in range(n):
		seq.append(choose_color(game))
	return seq

def generate_seq(game, n):
	return [random.choice(game["colors"].keys()) for _ in range(n)]

def show_seq(game, seq):
	def start_flow(trans):
		bulb.start_flow(Flow(count = 1, transitions = trans))
		time.sleep((len(trans)/2)*(game["delays"]["large"]+game["delays"]["small"]) / 1000.0)
		
	bulb.turn_on()
	time.sleep(game["delays"]["small"] / 1000.0)
	trans = []
	
	for c in seq:
		trans.append(RGBTransition(*game["colors"][c], duration = game["delays"]["large"]))
		trans.append(RGBTransition(*DEFAULT_COLOR, duration = game["delays"]["small"]))
		
		if trans >= 8:
			start_flow(trans)
			trans = []
	
	if len(trans) > 0:
		start_flow(trans)
		
def merge_dicts(d1, d2):
    dr = d1.copy()
    dr.update(d2)
    return dr

# -----------------------------------------------------------------

bulb = Bulb("192.168.1.133")

EASY_COLORS = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255)}
MEDIUM_COLORS = merge_dicts(EASY_COLORS, {"yellow": (255, 255, 0), "cyan": (0, 255, 255)})
HARD_COLORS = merge_dicts(EASY_COLORS, {"violet": (255, 0, 255)})

GAME_MODES = {"easy": {"colors": EASY_COLORS, "delays": {"large": 1000, "small": 100}}, \
			  "medium": {"colors": MEDIUM_COLORS, "delays": {"large": 800, "small": 100}}, \
			  "hard": {"colors": HARD_COLORS, "delays": {"large": 500, "small": 100}}}

DEFAULT_COLOR = (255, 255, 255)
INIT_NUM = 3

bulb.turn_on()
bulb.set_rgb(*DEFAULT_COLOR)

opt = None
while opt == None:
	print("Game mode:")
	for ind, gm in enumerate(GAME_MODES):
		print("%d) %s" % (ind+1, gm.capitalize()))

	try:
		opt = int(input("\n>>> "))
	except:
		print("\nInvalid color")
		
game = GAME_MODES[GAME_MODES.keys()[opt-1]]
seq = generate_seq(game, INIT_NUM)

while True:
	show_seq(game, seq)
	cseq = choose_seq(game, len(seq))

	if seq == cseq:
		print("Nice! Next round...")
		seq.append(random.choice(game["colors"].keys()))
	else:
		print("Fail! It was: %s" % ", ".join(seq))
		sys.exit(0)