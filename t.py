import usocket as socket
import network
import gc
import dht
from random import randint
from time import sleep



ssid = 'Kazimoto'
password = '$Yealink$'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass
print('Connection successfully')
print(station.ifconfig())


def web_page(distance):
    html = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Simple Parking System</title>
        </head>
        <body>
            <div id="container">
                <h1>Smart Parking System</h1>
                <p><strong>Available Parking Spot:</strong>  1 <br><strong>Total Parking Spot:</strong> 3</p>
                <div class="inner">
                    <div id="parking1">1</div>
                    <div id="parking2">2 </div>
                    <div id="parking3">3 </div>
                    <p>""" + str(distance) + """ </p>
                </div>
            </div>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Vollkorn:wght@400;500;700&display=swap');
                
                body{display: grid; font-family: 'Vollkorn', serif;background-color: #131313;}
                * {padding: 0;margin: 0;box-sizing: border-box;text-decoration: none;}
                h1{padding-top: 5%;}
                #container{margin-top: 10%;border: 2px solid black;border-radius: 30px;place-self: center;padding: 0 60px;height: 50%;background-color: beige;}
                .inner{padding: 4%;display: grid;grid-template-columns: repeat(auto-fit,minmax(50px, 1fr));grid-gap: 1rem;} 
                .inner>div{height: 7em; border-radius: 25px;display: flex;align-items: center;justify-content: center;}
                #parking1{background-color: blue}
                #parking2{background-color: rgb(255, 127, 127);}
                #parking3{background-color: rgb(255, 127, 127);}
            </style>
             <script>
             $(document).ready(
             function(){
             setInterval(function() {
             $('#inner');
             }, 2000); });
                distance = """ + str(distance) + """
                if ( distance  <=29){document.getElementById("parking1").style.backgroundColor='rgb(255, 127, 127)';
                }else{document.getElementById("parking1").style.backgroundColor='rgb(171, 231, 141)';}
                console.log(distance)
                
            </script>
        </body>
    </html>"""
    return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)



distance = randint(20,60)
while True:
    conn, addr = s.accept()
    print(' Got a connection from {}'.format(str(addr)))
    request = conn.recv(1024)
    request = str(request)
    print('Content = {}'.format(request))

    print(distance)
    d = randint(-10,1)
    distance = distance + d
    sleep(0.2)
    
   
    response = web_page(str(distance))
    
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
        

