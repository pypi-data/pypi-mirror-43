$( document ).ready(function() {
function checkCertidaoWidgets(){
    var tipo_widget = $('select[name="certidao-tipo"]');
    var cartorio_widget = $('input[name="certidao-cartorio"]');
    var livro_widget = $('input[name="certidao-livro"]');
    var folha_widget = $('input[name="certidao-folha"]');
    var data_widget = $('input[name="certidao-data"]');
    var municipio_widget = $('select[name="certidao-municipio"]');

    cartorio_widget.closest('.form-group').hide();
    livro_widget.closest('.form-group').hide();
    folha_widget.closest('.form-group').hide();
    data_widget.closest('.form-group').hide();
    municipio_widget.closest('.form-group').hide();

    var tipo = tipo_widget.val();
    if(tipo){
        if(tipo!='Novo Modelo'){
            cartorio_widget.closest('.form-group').show();
            console.log(cartorio_widget.closest('.form-group'));
            livro_widget.closest('.form-group').show();
            folha_widget.closest('.form-group').show();
            data_widget.closest('.form-group').show();
            municipio_widget.closest('.form-group').show();
        }
    }
 }
checkCertidaoWidgets();
    $('select[name="certidao-tipo"]').on('change', function(e) {
        checkCertidaoWidgets()
    });
});