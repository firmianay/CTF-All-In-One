require 'LFA'

$arr = LFA.new
$arr[1] = 11
$arr[5] = 11
$arr[15000] = 11
puts $arr.sum 


