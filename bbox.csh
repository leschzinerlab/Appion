#! /bin/csh -f

foreach file (*$1.box)
  set b=$file:r
  batchboxer input=$b.mrc dbbox=$file output=raw.hed newsize=$2 insideonly
  endif
end

proc2d raw.hed avg.mrc average
proc2d avg.mrc avg_c4.mrc sym=C4
proc2d avg_c4.mrc avg_c4_dc2.mrc meanshrink=2

