#! /bin/csh -f

if (! -e boxed.lst) then
	    touch boxed.lst
endif

set numfiles = `ls *$1.mrc | wc -l`
echo $numfiles $1 files found

foreach file (*$1.mrc)
	set b=$file:r
	set check=`grep $file boxed.lst`
	if ($check == "") then
        	echo ""
        	echo $b.box
		echo ""
        	boxer $file scale=0 contrast=0.4
        	echo $file >> boxed.lst
		set numboxed = `cat *.box | wc -l`
		echo $numboxed boxed so far
		set numfilesdone = `cat boxed.lst | wc -l`
		@ numleft = $numfiles - $numfilesdone
		echo $numleft files left	
	endif
end


