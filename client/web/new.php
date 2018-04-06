<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=2.0, user-scalable=yes"/>
    <meta name="apple-mobile-web-app-capable" content="yes"/>
    <meta name="format-detection" content="telephone=no"/>
    <style>
        .error {
            color: #FF0000;
        }
    </style>
</head>
<body>
<?php
$db = new SQLite3('/home/minecraft/Information System/server/data.db');
for ($i = 0; $i < count($_POST["select"]); $i++) {
    $id = $_POST["select"][$i];
    $db->exec("update new set isRead=1 where id={$id}");
    if ($_POST["exec"]=="star"){
        $belong = "favorite";
        $insert = $db->exec("insert into '{$belong}' SELECT * from new where id='{$id}'");
    }
//    elseif ($_POST["exec"]=="submit"){
//        $belong = substr($_POST["select"][$i], 20);
//        $insert = $db->exec("insert into '{$belong}' SELECT id,title,url,weight from new where id='{$id}'");
//    }
//
//    $insert = $db->exec("delete from new where id='{$id}'");

}


?>
<form action='new.php' method='POST'>
    <table align='center'>
        <tr>
            <td colspan="4">
                <input type="button" id="All" value="全选"/>
                <input type="button" id="uncheck" value="不选"/>
                <input type="button" id="othercheck" value="反选"/></td>
        </tr>

        <?php
        /**
         * Created by PhpStorm.
         * User: minecraft
         * Date: 16-9-3
         * Time: 下午9:50
         */


        $result = $db->query("select * from new where isRead=0");
        while ($row = $result->fetchArray()) {
            if ($row["isRead"] == 0) {

                echo "<tr><td rowspan='2'><input type='checkbox' name='select[]' value=" . $row["id"] . "></td>";
                echo "<td colspan='2'>" . $row["belong"] . "</td></tr>";
                echo "<tr><td>" . $row["id"] . "</td>";
                echo "<td><a href=" . $row["url"] . ">" . $row["title"] . "</a></td>";
                echo "<td>" . $row["isRead"] . "</td></tr>";
            }
        }

        $db->close();
        ?>

        <tr>
            <td colspan="1"><input type="submit" name='exec' value="submit"></td>
            <td colspan="1"><input type="submit" name='exec' value="star"></td>
        </tr>
    </table>
</form>
<script>
    window.onload = function () {
        var CheckAll = document.getElementById('All');
        var UnCheck = document.getElementById('uncheck');
        var OtherCheck = document.getElementById('othercheck');
        var CheckBox = document.getElementsByName('select[]');
        CheckAll.onclick = function () {
            for (i = 0; i < CheckBox.length; i++) {
                CheckBox[i].checked = true;
            }
            ;
        };
        UnCheck.onclick = function () {
            for (i = 0; i < CheckBox.length; i++) {
                CheckBox[i].checked = false;
            }
            ;
        };
        OtherCheck.onclick = function () {
            for (i = 0; i < CheckBox.length; i++) {
                if (CheckBox[i].checked == true) {
                    CheckBox[i].checked = false;
                }
                else {
                    CheckBox[i].checked = true
                }

            }
            ;
        };
    };
</script>
</body>
</html>
