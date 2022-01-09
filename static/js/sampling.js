let table = document.getElementById("table_sampling")

function build(data) {

    if(typeof(data.msg) === 'object') {
        
    } else{
        table.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>`+data.msg+`</strong>
        </div>
        `
    }
}