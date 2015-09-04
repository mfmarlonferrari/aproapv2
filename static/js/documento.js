$(function(){
	var editor, html = '';		

	var ConfigCalendar = {
		
		defineIdioma : function(){
			$('.date').datepicker({                                  
            	language: 'pt-BR',
            	dates:{
		            days: ['Domingo','Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado'],
		            daysShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'],
		            daysMin: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'],
		            months: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
		            monthsShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        		}
        		
            });
		},

		defineDataInicial: function(){
			$(".date").datepicker("update", new Date());
		},

	}

	var FkEditor ={

		// Verifica se o usuário destacou parte do texto
		existeTextoEmDestaque : function(textoHtml){

			if($(textoHtml).hasClass('marker'))
				return true

			return false;		
		},	

		createEditor : function () {
			if ( editor )
				return;

			// Create a new editor inside the <div id="editor">, setting its value to html
			var config = {};
			editor = CKEDITOR.appendTo( 'editor', config, html );

			$('#contents' ).hide();
		},

		removeEditor: function () {

			if ( !editor )
				return;

			// Retrieve the editor contents. In an Ajax application, this data would be
			// sent to the server or used in any other way.
			html = editor.getData();

			$('#editorcontents').html(editor.getData());
			
			$('#contents' ).show();
			$('#resumo_em_html').val(html);		

			// Destroy the editor.
			editor.destroy();
			editor = null;		
		}
	

	};
		
	var Documento = {
		classificar: function(object){
			if($(object).hasClass('star-decolorize')){
				$(object).removeClass('star-decolorize');
				$(object).addClass('star-colorize');
			}
			else{
				$(object).removeClass('star-colorize');
				$(object).addClass('star-decolorize');
			}
		},

		atribuirClassificacao:function(){
			$('#classificacao').val($('.star-colorize').length);								
		},

		rolarScrollPagina:function(){

   		 	var target_offset = $("#salvar").offset().top;    	    	
    		$('html, body').animate({ scrollTop: target_offset }, 1400);   
		}
	};



	var Event = {

		classificarArtigo: function(){		
			$('.classifica').click(function(){			
				Documento.classificar(this);
				Documento.atribuirClassificacao();						
			});
		},

		finalizarEdicaoResumo : function(){

			$('.cancelar-resumo').click(function(){				
				FkEditor.removeEditor();
			});		
		},	

		criarResumo : function(){			

			$('.criar-resumo').click(function(){				
				FkEditor.createEditor();				
				Documento.rolarScrollPagina();
			});		
		}
		
	};	

	App = {

		init:function()
		{			

			Event.classificarArtigo();	
			Event.criarResumo();		
			Event.finalizarEdicaoResumo();

			ConfigCalendar.defineIdioma();
			ConfigCalendar.defineDataInicial();
	
		}
	};
		
	
	App.init();
});