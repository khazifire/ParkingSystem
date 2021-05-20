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


def web_page(distance1,distance2,distance3,counter):
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
            <p>Available Spot: <strong>"""+(counter)+"""</strong></p>
            <p>Total Spot: 3</p>
            <div class="inner" id="inb">
                <div id="parking1"><img id="car1" src="https://github.com/dankazim/ParkingSystem/blob/main/car.png?raw=true" alt=""></div>
                <div id="parking2"><img id="car2" src="https://github.com/dankazim/ParkingSystem/blob/main/car.png?raw=true" alt=""></div>
                <div id="parking3"><img id="car3" src="https://github.com/dankazim/ParkingSystem/blob/main/car.png?raw=true" alt=""></div> 
            </div>
        </div>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Vollkorn:wght@400;500;700&display=swap');
            :root{--green:rgb(171, 231, 141); --red:rgb(255, 127, 127);}
            body{display: grid; font-family: 'Vollkorn', serif;background-color: #131313;}
            * {padding: 0;margin: 0;box-sizing: border-box;text-decoration: none;}
            h1{padding-top: 5%;}
            #container{margin-top: 10%;border: 2px solid black;border-radius: 30px;place-self: center;padding: 0 60px;height: 50%;background-color: beige;}
            .inner{padding: 4%;display: grid;grid-template-columns: repeat(auto-fit,minmax(50px, 1fr));grid-gap: 1rem;} 
            .inner>div{height: 7em; border-radius: 25px;display: flex;align-items: center;justify-content: center;}
            #parking1{background-color:var(--green);}
            #parking2{background-color: var(--green);}
            #parking3{background-color: var(--green);}
            img{ height:90%;}
            p strong {background-color: var(--green);padding: 2px 7px 2px 7px;border-radius: 50%;color: rgb(0, 0, 0);
        </style>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"> </script>
        <script>
                distance1 = """ + str(distance1) + """
                distance2 = """ + str(distance2) + """
                distance3 = """ + str(distance3) + """
                
                if ( distance1  <=29){
                document.getElementById("parking1").style.backgroundColor='rgb(255, 127, 127)';
                document.getElementById("car1").style.visibility = "visible";
                }else{document.getElementById("parking1").style.backgroundColor='rgb(171, 231, 141)';
                document.getElementById("car1").style.visibility = "hidden";}
                
                if ( distance2  <=29){
                document.getElementById("parking2").style.backgroundColor='rgb(255, 127, 127)';
                document.getElementById("car2").style.visibility = "visible";
                }else{document.getElementById("parking2").style.backgroundColor='rgb(171, 231, 141)';
                document.getElementById("car2").style.visibility = "hidden";}

                if ( distance3  <=29){
                document.getElementById("parking3").style.backgroundColor='rgb(255, 127, 127)';
                document.getElementById("car3").style.visibility = "visible";
                }else{document.getElementById("parking3").style.backgroundColor='rgb(171, 231, 141)';
                document.getElementById("car3").style.visibility = "hidden";}
                
                setInterval(()=>{location.reload(); }, 3000)
        </script>
    </body>
    </html>"""
   return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

counter = 0
while True:
    conn, addr = s.accept()
    print(' Got a connection from {}'.format(str(addr)))
    request = conn.recv(1024)
    request = str(request)
    
    distance1 = randint(25,35)
    distance2 = randint(28,40)
    distance3 = randint(23,35)
    print(distance1,distance2,distance3)

    if (distance1 >=30 and distance2 >=30) and distance3 >=30:
        counter =3
    elif (distance1 >=30 and distance3 >=30) or (distance2 >=30  and distance3 >=30)or(distance1 >=30 and distance2 >=30):
        counter =2
    elif distance1 >=30  or distance2 >=30  or distance3 >=30 :
        counter =1
    else:
        counter = 0
    
    sleep(0.2)
    
    response = web_page(str(distance1),str(distance2),str(distance3),str(counter))
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
        


