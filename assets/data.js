// Asignaturas PAES. estado: "disponible" | "pronto"
const ASIGNATURAS = [
  {id:"biologia",nombre:"Biología",ico:"🧬",desc:"Ciencias – Módulo Biología",estado:"disponible",capitulos:[]},
  {id:"fisica",nombre:"Física",ico:"⚛️",desc:"Ciencias – Módulo Física",estado:"disponible",capitulos:[
    "Ondas: características y clasificación","El sonido","La luz y la óptica geométrica","Sismos y dinámica de la Tierra",
    "Cinemática: descripción del movimiento","Dinámica: fuerzas y leyes de Newton","Movimiento circular uniforme",
    "Trabajo, potencia y energía mecánica","Momentum lineal e impulso","Calor y temperatura",
    "Electricidad y circuitos eléctricos","Magnetismo y electromagnetismo","La Tierra y el Universo"]},
  {id:"quimica",nombre:"Química",ico:"🧪",desc:"Ciencias – Módulo Química",estado:"disponible",capitulos:[
    "Modelos atómicos y estructura del átomo","Configuración electrónica y números cuánticos","Tabla periódica y propiedades periódicas",
    "Enlace químico","Geometría molecular y fuerzas intermoleculares","Nomenclatura inorgánica",
    "Leyes ponderales y concepto de mol","Reacciones químicas y estequiometría","Disoluciones químicas",
    "Propiedades coligativas","Química orgánica: el átomo de carbono","Grupos funcionales y nomenclatura orgánica",
    "Isomería y reactividad orgánica"]},
  {id:"lectora",nombre:"Competencia Lectora",ico:"📖",desc:"Comprensión lectora",estado:"pronto",capitulos:[]},
  {id:"m1",nombre:"Matemática M1",ico:"➗",desc:"Competencia Matemática 1",estado:"pronto",capitulos:[]},
  {id:"m2",nombre:"Matemática M2",ico:"📐",desc:"Competencia Matemática 2",estado:"pronto",capitulos:[]},
  {id:"historia",nombre:"Historia y Cs. Sociales",ico:"🏛️",desc:"Historia, Geografía y Cs. Sociales",estado:"pronto",capitulos:[]}
];
function requireLogin(){ try{ if(!sessionStorage.getItem("usuario")) location.href="login.html"; }catch(e){} }
