input_file="$1"
pcm_file="${input_file%.*}.pcm"
amr_file="${input_file%.*}.amr"

cur_dir=$(dirname "$0")

# echo "input_file: $input_file"
# echo "pcm_file: $pcm_file"
# echo  "amr_file: $amr_file"

ffmpeg -i "$input_file" -f s16le -ar 24000 -ac 1 -acodec pcm_s16le  "$pcm_file"

$cur_dir/silk_encoder "$pcm_file" "$amr_file" -tencent
rm "$pcm_file"
