if [ -e "traffic_log.txt" ]
then
	echo "removing traffic_log.txt..."
	rm traffic_log.txt
fi

if [ -e "dst_num_distribution.txt" ]
then
	echo "removing dst_num_distribution.txt..."
	rm dst_num_distribution.txt
fi

if [ -e "src_num_distribution.txt" ]
then
	echo "removing src_num_distribution.txt..."
	rm src_num_distribution.txt
fi

if [ -e "dst_rack_distribution.txt" ]
then
	echo "removing dst_rack_distribution.txt..."
	rm dst_rack_distribution.txt
fi

if [ -e "src_rack_distribution.txt" ]
then
	echo "removing src_rack_distribution.txt..."
	rm src_rack_distribution.txt
fi
