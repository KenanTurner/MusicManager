<?php
	$data = json_decode(file_get_contents('php://input'), true);
	$url = $data["href"];

	$doc = new DOMDocument();
	$doc->loadHTMLFile($url,LIBXML_COMPACT);
	$h1 = $doc->getElementsByTagName("script");
	$hrefs = array();
	//echo count($h1);
	foreach ($h1 as $h) {
		$tmp = $h->getAttribute('data-tralbum');
		if($tmp==NULL){
			continue;
		}
		$tmpJson = json_decode($tmp,true);
		foreach($tmpJson["trackinfo"] as $x){
			//echo $x["file"]["mp3-128"], PHP_EOL;
			$hrefs[$x["title"]] =$x["file"]["mp3-128"];
		}
		//echo trim($tmpJson["trackinfo"][0]["file"]["mp3-128"]);
	}
	echo json_encode($hrefs);
?>
