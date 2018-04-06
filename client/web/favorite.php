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

?>
    <table align='center'>

        <?php
        /**
         * Created by PhpStorm.
         * User: minecraft
         * Date: 16-9-3
         * Time: 下午9:50
         */


        $result = $db->query("select * from favorite ");
        while ($row = $result->fetchArray()) {

                echo "<tr><td colspan='2'>" . $row["belong"] . "</td></tr>";
                echo "<tr><td><a href=" . $row["url"] . ">" . $row["title"] . "</a></td></tr>";
            }

        $db->close();
        ?>
    </table>
</body>
</html>
