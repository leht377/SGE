const modales = document.getElementById('ventanaModal');
const btncrearEmpleado = document.getElementById('crearEmpleado') ;
const closeModal = document.getElementById('CerrarModal');

btncrearEmpleado.addEventListener('click',() =>{
   modales.style.transition = 'transition: all 0.35s ease';
   modales.style.marginTop = '0';

});

closeModal.addEventListener('click',()=> {
    modales.style.marginTop = '-200vh';
});

