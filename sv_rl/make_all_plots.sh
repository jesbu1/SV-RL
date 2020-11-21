#/bin/bash
sh make_plots.sh breakout svt &
sh make_plots.sh breakout softimp &
sh make_plots.sh breakout iterative_svd &
sh make_plots.sh frostbite svt &
sh make_plots.sh frostbite softimp &
sh make_plots.sh frostbite iterative_svd & 
