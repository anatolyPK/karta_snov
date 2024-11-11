import dash_bootstrap_components as dbc
from dash import Dash

from src.callbacks import *
from src.page import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

server = app.server

app.layout = layout
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
            <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-Z51CXJCRKE"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-Z51CXJCRKE');
        </script>
            
                <!-- Yandex.Metrika counter -->
        <script type="text/javascript" >
           (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
           m[i].l=1*new Date();
           for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
           k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
           (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
        
           ym(98878756, "init", {
                clickmap:true,
                trackLinks:true,
                accurateTrackBounce:true
           });
        </script>
        <noscript><div><img src="https://mc.yandex.ru/watch/98878756" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
        <!-- /Yandex.Metrika counter -->

        {%metas%}
        <title>Карта Снов | Учебная топографическая карта У-34-37-В (СНОВ) 1:50000</title>
        <meta name="description" content="Карта Снов У-34-37-В - интерактивная карта, позволяющая определять 
        географические координаты, полные и сокращенные координаты объектов, номенклатуру смежных листов топографической
        карты, магнитный азимут направления, расстояние между объектами, целеуказание от условной линии на цель.">
        <meta name="keywords" content="карта, Снов, карта Снов, У-34-37-В, у-34-37-в, географические координаты, 
        полные прямоугольные координаты, сокращенные прямоугольные координаты, номенклатура, 
        расстояние, магнитный азимут, целеуказание, интерактивное приложение">
        <meta name="author" content="Борис">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="assets/kompas.ico" type="image/png">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True)
