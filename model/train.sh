# $1 -> Dataset ,$3 -> Rank, $2 -> MaxIter , $4 -> Save Model
matlab -nodisplay -nosplash -nodesktop -r \
 "try, addpath('/home/sanket/cs6604/tensorlab_2016-03-28'); , addpath('/home/sanket/cs6604/code'); ,trainStore('$1', $2,  $3 , '$4',$5) , catch me, fprintf('%s / %s\n',me.identifier,me.message), end, exit"