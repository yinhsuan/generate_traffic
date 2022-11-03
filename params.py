
NUM_OF_PODS = 3
NUM_OF_RACKS_PER_POD = 5

MIN_RACK_NUM = 1
MAX_RACK_NUM = 15

MIN_SERVER_ID = 16
MAX_SERVER_ID = 31

MIN_SERVER_NUM = 1
MAX_SERVER_NUM = 16

START_PORT = 7000

# User Parameters
CASE = "locality" # <fixed>/ <whole>/ <locality>
TRAFFIC_FILE = "tmp.txt"
FLOW_MEAN = 0.05
FLOW_STD = 0.03
SCALE = 100.0 # number MUST larger than 0
DST_RACK_MEAN = 8.0 # if user do not want to define => set: 0.0
DST_RACK_STD = 2.0
PROTOCOL = "u"
IPERF_VERSION = "iperf"