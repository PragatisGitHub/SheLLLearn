      
function random_upper(){
var UpperLetterCards=new Array()
//specify random images below. You can have as many as you wish
UpperLetterCards[0] = 'CapitalA.png'
UpperLetterCards[1] = 'CapitalB.png'
UpperLetterCards[2] = 'CapitalC.png'
UpperLetterCards[3] = 'CapitalD.png'
UpperLetterCards[4] = 'CapitalE.png'
UpperLetterCards[5] = 'CapitalF.png'
UpperLetterCards[6] = 'CapitalG.png'
UpperLetterCards[7] = 'CapitalH.png'
UpperLetterCards[8] = 'CapitalI.png'
UpperLetterCards[9] = 'CapitalJ.png'
UpperLetterCards[10] = 'CapitalK.png'
UpperLetterCards[11] = 'CapitalL.png'
UpperLetterCards[12] = 'CapitalM.png'
UpperLetterCards[13] = 'CapitalN.png'
UpperLetterCards[14] = 'CapitalO.png'
UpperLetterCards[15] = 'CapitalP.png'
UpperLetterCards[16] = 'CapitalQ.png'
UpperLetterCards[17] = 'CapitalR.png'
UpperLetterCards[18] = 'CapitalS.png'
UpperLetterCards[19] = 'CapitalT.png'
UpperLetterCards[20] = 'CapitalU.png'
UpperLetterCards[21] = 'CapitalV.png'
UpperLetterCards[22] = 'CapitalW.png'
UpperLetterCards[23] = 'CapitalX.png'
UpperLetterCards[24] = 'CapitalY.png'
UpperLetterCards[25] = 'CapitalZ.png'

var ry=Math.floor(Math.random()*UpperLetterCards.length)
if (ry==0)
ry=1
document.write('<img src="../Images/upperlettercards/'+UpperLetterCards[ry]+'" border=0, class="img-responsive"')
}
random_upper()
