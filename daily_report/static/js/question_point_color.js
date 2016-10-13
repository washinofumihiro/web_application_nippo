function select_question(obj){
    var select_question = window.getSelection();

    if (select_question == '') {return false;}

    alert(select_question);
    var base_word = 'id_question_';
    var id_word = base_word + obj.id;
//    alert(id_word);
    var question_level = document.getElementById(id_word);
//    var select_range = select_question.getRangeAt(0);
//    var span = document.createElement("span");
//    alert(span.value);
//    question_level.value = span.value;
    question_level.value = select_question;

//    span.style.color = "#ff0000";
//    select_range.surroundContents(span);


//色を変える
//    var select_question = window.getSelection();
//
//    if (select_question == '') {return false;}
//
//    var select_range = select_question.getRangeAt(0);
//    var span = document.createElement("span");
//
//    span.style.color = "#ff0000";
//    select_range.surroundContents(span);
}
