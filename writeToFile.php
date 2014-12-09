<html>
<style>
body {
	color: white;
	background: #ffffff url("assets/imgs/dota2bg.jpg") no-repeat top center;
	background-attachment: fixed;
	background-color: gray;
	background-size: 1080px 1050px;
}
</style>
<body>
<?php
if(isset($_POST['field1'])) {
    $data = $_POST['field1'] . "\n";
	$filedescriptor = fopen('user.txt', 'w');
	fwrite($filedescriptor, $data);
	fclose($file);
}
   
   exec('/Users/zoetrope92/anaconda/bin/python assets/crawler/playerProfileCreatorMRJob.py user.txt > assets/profile.json');
   
   exec('/Users/zoetrope92/anaconda/bin/python assets/playerComparison.py > assets/results.json', $output, $return);
   
   /*foreach ($output as $errorVal){
	   echo $errorVal;
   }*/
	
   $filename = 'assets/results.json';
   $filedescriptor = fopen($filename, 'r');
   $results = fread($filedescriptor, filesize($filename));
   fclose($filedescriptor);
   $json = json_decode($results);
	
	echo(
	"<center><br><br><br><h1>Recommended Unplayed Heroes</h1>".
	"<table>".
	"<tbody>".
	"<tr>".
	
    "<th>Image</th><th>Hero</th>
    <th><center>Predicted Win %</center></th>
	<th><center>Predicted KDA Ratio</center></th>
  	</tr>");
	foreach ($json as $hero) {
		echo( "<tr>
		<td><a href=\"http://www.dota2.com/hero/" . $hero->{'hero_link'} . "/\"><img src=\"//cdn.dota2.com/apps/dota2/images/heroes/" . $hero->{'formatted_name'} . 
		"_hphover.png\" alt=\"Hero image\" style=\"width:127px;height:71px\"></a></td>
		<td><center>" . $hero->{'hero_name'} . "</center></td>
		<td><center>" . $hero->{'win_perc'} . "</center></td>
		<td><center>" . $hero->{'kda'} . "</center></td>
		</tr>");
	}
	echo("</tbody>" . "</table><br><br><br><br></center>");
	
?>
</body>
</html>