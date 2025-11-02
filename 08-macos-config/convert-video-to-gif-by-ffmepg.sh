#!/bin/bash
# Program:
#   convert video to gif file by using ffmepg
# History:
#   DeltaV235 2023-01-31 create shell script

# default value
width=1280
rate=12
loop=0

Help() {
    echo
    echo "Usage:"
    echo "  bash convert-video-to-gif-by-ffmepg.sh [options] {-i input_video} {-o output_video}"
    echo
    echo "options:"
    echo "  -t create how many second output"
    echo "  -w width of ouput gif (Default: 1280px"
    echo "  -r frame rate of gif (Default: 12FPS)"
    echo "  -l loop time (Default: 0 - infinite looping)"
    echo
}

while getopts hi:o:t:w:r:l: option
do
    case "${option}" in
        i) input=${OPTARG};;
        o) output=${OPTARG};;
        t) time=${OPTARG};;
        w) width=${OPTARG};;
        r) rate=${OPTARG};;
        l) loop=${OPTARG};;
        h) Help; exit;;
        \?) echo "Error: Invalid Option"; exit;;
    esac
done

ffmpeg -i "${input}" -t ${time} -r ${rate} -vf "scale=${width}:-1" -loop 0 "${output}"
