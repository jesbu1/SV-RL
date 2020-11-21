#!/bin/bash
ENV=$1
METHOD=$2
python plot.py data/"$ENV"_dqn_svrl_"$METHOD"_0.5_16 data/"$ENV"_dqn_svrl_"$METHOD"_0.5_32 data/"$ENV"_dqn_svrl_"$METHOD"_0.5_64 data/"$ENV"_dqn_svrl_"$METHOD"_0.9_16 data/"$ENV"_dqn_svrl_"$METHOD"_0.9_32 data/"$ENV"_dqn_svrl_"$METHOD"_0.9_64 --legend 0.5_16 0.5_32 0.5_64 0.9_16 0.9_32 0.9_64 --title "$METHOD"_"$ENV"_Comparison --save_name "$METHOD"_"$ENV"_comparison

