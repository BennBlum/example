# Create the data directory with appropriate permissions
sudo mkdir -p /mnt/data
sudo chmod 777 /mnt/data

# Download and decrypt data
start_time="$(date -u +%s)"
echo "Downloading data: $start_time"
python3 $build_dir/download_decrypt_zip.py
end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Download completed: $elapsed seconds"

# Start the training process
start_time="$(date -u +%s)"
echo "Training started: $start_time"

docker run -it --gpus all -p 8000:8000 --shm-size=256m \
    -v /mnt/data:/mnt/data --rm $train_image \
    python3 $app_dir/trainer.py \
    --hf-path $hf_path \
    --chkpt-path $chkpt_path \
    --data-path $data_path \
    --chkpt $chkpt_name \
    --epochs $epochs \
    --patience $patience

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Training completed: $end_time"
echo "Training time: $elapsed seconds"

# Start the evaluation process
start_time="$(date -u +%s)"
echo "Evaluation started: $start_time"

docker run -it --gpus all -p 8000:8000 --shm-size=256m \
    -v /mnt/data:/mnt/data --rm $train_image \
    python3 $app_dir/evaluator.py \
    --data-path $data_path \
    --chkpt $chkpt_name

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Evaluation completed: $end_time"
echo "Evaluation time: $elapsed seconds"