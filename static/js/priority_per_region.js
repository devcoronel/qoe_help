let region = document.getElementById("region")

region.addEventListener('change', function(e){
  e.preventDefault();

  fetch('/priority' , {
	method: 'POST',
	body: JSON.stringify(
            region.value
        )
	})
    .then(response => response.json())
		.then(data => {
      if(typeof(data.msg) === 'object') {
        build(data)
      } else{
        div_generaltable.innerHTML = data.msg
        div_especifictable.innerHTML = data.msg
      }
    })
    .catch(err => {
      div_generaltable.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
      <strong>Se detectó excesivas peticiones a la Base de Datos en un tiempo corto. Intentar de nuevo</strong>
      </div>
      `
      div_especifictable.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
      <strong>Se detectó excesivas peticiones a la Base de Datos en un tiempo corto. Intentar de nuevo</strong>
      </div>
      `
    })
})