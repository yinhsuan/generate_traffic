read -p "Enter dst_rack_mean: " mean
read -p "Enter dst_rack_std: " std
read -p "Enter iteration_num: " it_num

./clean_log_file.sh

if [ "$mean" -gt 0 ]
then
    echo "dst_rack_num distribution: Truncated-normal"
else
    echo "dst_rack_num distribution: Uniform"
fi

for i in $(seq 1 1 $it_num)
do
    echo "iteration {$i}, generating traffics..."
    python3 generate_traffic.py

    echo "Parsing log file..."
    python3 log_file_verify.py

    rm traffic_log.txt
done

echo -e "\nVerifying dst. rack number distribution...\n"
python3 locality_distribution_verify.py

echo "=============== Verification finished !!! ================="
