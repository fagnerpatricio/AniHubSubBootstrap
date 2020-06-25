function t (doc) {
        emit(doc.timestamp,{titulo:doc.titulo,thumb:doc.cod_thumb,legenda:doc.url_legendas,inicio:doc.inicio_de_exibicao, fim:doc.final_de_exibicao,links:doc.link_externos});
}
    