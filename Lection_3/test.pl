use 5.010;
$number = 2;
for $i (1..500) {
	say $i;
	$result = `echo "$number\n$i\n" | python3 Task_2.py`;
	say $result;
}
