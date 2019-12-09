OMP_THREAD_LIMIT=8 lstmtraining \
    --continue_from jpn.lstm \
    --model_output pxj-output/pxj \
    --traineddata tessdata_best/jpn.traineddata \
    --train_listfile pxjtrain/jpn.training_files.txt \
    --max_iterations 2000
