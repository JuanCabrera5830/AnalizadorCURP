function generarCURP(nombre, apellido1, apellido2, fecha, sexo, estado) {
  nombre = nombre.trim().toUpperCase();
  apellido1 = apellido1.trim().toUpperCase();
  apellido2 = apellido2.trim().toUpperCase();
  sexo = sexo.toUpperCase();
  estado = estado.toUpperCase();

  function primerVocalInterna(palabra) {
    for (let i = 1; i < palabra.length; i++) {
      if ("AEIOU".includes(palabra[i])) {
        return palabra[i];
      }
    }
    return "X";
  }

  function primeraConsonanteInterna(palabra) {
    for (let i = 1; i < palabra.length; i++) {
      if (!"AEIOU".includes(palabra[i]) && /[A-Z]/.test(palabra[i])) {
        return palabra[i];
      }
    }
    return "X";
  }

  let curp = apellido1[0];
  curp += primerVocalInterna(apellido1);
  curp += apellido2 ? apellido2[0] : "X";
  curp += nombre[0];

  const [anio, mes, dia] = fecha.split("-");
  curp += anio.slice(2) + mes + dia;
  curp += sexo;

  const estados = {
    "AGUASCALIENTES": "AS", "BAJA CALIFORNIA": "BC", "BAJA CALIFORNIA SUR": "BS",
    "CAMPECHE": "CC", "COAHUILA": "CL", "COLIMA": "CM", "CHIAPAS": "CS",
    "CHIHUAHUA": "CH", "CIUDAD DE MEXICO": "DF", "DURANGO": "DG", "GUANAJUATO": "GT",
    "GUERRERO": "GR", "HIDALGO": "HG", "JALISCO": "JC", "ESTADO DE MEXICO": "MC",
    "MICHOACAN": "MN", "MORELOS": "MS", "NAYARIT": "NT", "NUEVO LEON": "NL",
    "OAXACA": "OC", "PUEBLA": "PL", "QUERETARO": "QT", "QUINTANA ROO": "QR",
    "SAN LUIS POTOSI": "SP", "SINALOA": "SL", "SONORA": "SR", "TABASCO": "TC",
    "TAMAULIPAS": "TS", "TLAXCALA": "TL", "VERACRUZ": "VZ", "YUCATAN": "YN",
    "ZACATECAS": "ZS", "NACIDO EN EL EXTRANJERO": "NE"
  };

  curp += estados[estado] || "NE";

  curp += primeraConsonanteInterna(apellido1);
  curp += primeraConsonanteInterna(apellido2);
  curp += primeraConsonanteInterna(nombre);

  curp += (parseInt(anio) > 1999) ? "A0" : "00";

  return curp;
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const resultDiv = document.querySelector(".result");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nombre = form.nombre.value;
    const apellido1 = form.apellido1.value;
    const apellido2 = form.apellido2.value;
    const fecha = form.fecha.value;
    const sexo = form.sexo.value;
    const estado = form.estado.value;

    const curp = generarCURP(nombre, apellido1, apellido2, fecha, sexo, estado);

    resultDiv.innerHTML = `
      <h2>CURP generado:</h2>
      <p><strong>${curp}</strong></p>
    `;
  });
});