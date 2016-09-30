function select_question(){
    var select_question = window.getSelection();

    if (select_question == '') {return false;}

    var select_range = select_question.getRangeAt(0);
    var span = document.createElement("span");

    span.style.color = "#ff0000";
    select_range.surroundContents(span);
}
