<!DOCTYPE html>
<html>
    <head>
        <style type="text/css">
            body {
                font-family:arial;
                font-size:0.2cm;
               
            }
               
            table {
                width:100%;
                margin-left:auto;
                margin-right:auto;
                padding: 2px;       
                text-align:center;
                -webkit-border-radius: 10px;
                       
            }
           
           
        </style>
    </head>

 <body>

<header>
        <table>
            <tr><td align="left">${helper.embed_logo_by_name('nombredelaimagen', width=90)|n}</td>       
         </tr>
        </table>
    </header>

%for object in objects:
     <table border="1" cellpadding="2" cellspacing="2">

         <tr>
                    <td style="vertical-align: top;">
                        ${object.id}<br>
                    </td>
                    <td style="vertical-align: top;">
                        ${object.name}<br>
                    </td>
                    <td style="vertical-align: top;">
                        ${object.name}<br>
                    </td>
                    <td style="vertical-align: top;">
                        ${object.name}<br>
                    </td>
                    <td style="vertical-align: top;">
                            ${object.name}
                      
                    </td>
                    <td style="vertical-align: top;">
                            ${object.name}<br>
                    </td>
                    <td style="vertical-align: top;">
                                       ${object.name}-<br>
                    </td>
         </tr>
     </table>

  %endfor
 </body>
</html>