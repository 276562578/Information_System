<?php
/**
 * Created by PhpStorm.
 * User: minecraft
 * Date: 17-5-30
 * Time: 下午6:46
 */
$db = new SQLite3('/home/minecraft/Information System/server/data.db');
$result = $db->query("select * from new where isRead=0");
$data = array();
$i=0;
while ($row = $result->fetchArray()) {


    if ($row["isRead"] == 0) {
        $subData["id"]=$row["id"];
        $subData["belong"]=$row["belong"];
        $subData["url"]=$row["url"];
        $subData["title"]=$row["title"];
    }
    $data[$i]=$subData;
    $i++;
}
echo json_encode($data);
$db->close();
?>