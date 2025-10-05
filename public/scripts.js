document.getElementById('curp-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const form = e.target;

  const datos = {
    nombre: form.nombre.value,
    apellido1: form.apellido1.value,
    apellido2: form.apellido2.value,
    fecha: form.fecha.value,
    sexo: form.sexo.value,
    estado: form.estado.value
  };

  const res = await fetch('/api', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });

  const curpCuadro = document.getElementById('curp-cuadro');
  const erroresBox = document.getElementById('errores-box');
  curpCuadro.innerHTML = '';
  erroresBox.innerHTML = '';

  const respuesta = await res.json();

  if (res.ok) {
    curpCuadro.innerHTML = `
      <div class="result">
        <h2>CURP Generada:</h2>
        <p><strong>${respuesta.curp}</strong></p>
      </div>
    `;
  } else {
    const errs = respuesta.errores || ['Error desconocido'];
    erroresBox.innerHTML = `
      <div class="errors">
        <ul>${errs.map(e => `<li>${e}</li>`).join('')}</ul>
      </div>
    `;
  }
});