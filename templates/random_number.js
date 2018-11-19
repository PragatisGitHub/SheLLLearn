      
function random_number(){
var NumberCards=new Array()
//specify random images below. You can have as many as you wish
NumberCards[0] = 'number0.png'
NumberCards[1] = 'number1.png'
NumberCards[2] = 'number2.png'
NumberCards[3] = 'number3.png'
NumberCards[4] = 'number4.png'
NumberCards[5] = 'number5.png'
NumberCards[6] = 'number6.png'
NumberCards[7] = 'number7.png'
NumberCards[8] = 'number8.png'
NumberCards[9] = 'numberf9.png'


var ry=Math.floor(Math.random()*NumberCards.length)
if (ry==0)
ry=1
document.write('<img src="../Images/upperlettercards/'+NumberCards[ry]+'" border=0, height=300>')
}
random_number()
