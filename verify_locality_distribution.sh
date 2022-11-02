read -p "Enter dst_rack_mean" mean
read -p "Enter dst_rack_std" std

for i in $(seq 1 1 100)
do
    echo "iteration {$i}, generating traffics..."
    python3 generate_traffic.py --case locality --mean 5 --std 3 --traffic_file tmp.txt --scale 100 --dst_rack_mean $mean --dst_rack_std $std

    echo "parsing log file..."
    python3 log_file_verify.py --mean 5 --std 3 --scale 100    

    rm traffic_log.txt
done

echo "verifying dst. rack number distribution..."
python3 locality_distribution_verify.py

rm locality_distribution.txt