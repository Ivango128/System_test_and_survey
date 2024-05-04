const plusNode = document.querySelector('.btn__plus')
const cont_answersNode = document.querySelector('.cont__for__answers')

const isClosedNode = document.querySelector('#closed_question')
const isOpenNode = document.querySelector('#open_question')

const groupNode = document.querySelector('.cont__radio__hiden')
const groupAnswers = document.querySelector('.block__answers')
const oneAnswer = document.querySelector('.block__one__answer')


const isAnylistNode = document.querySelector('#any_list')
const isOnelistNode = document.querySelector('#one_list')


const oneAnswerNode = document.querySelector('.input__title__create')

let list_answers = [];

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

const get_answer_failed = (answer_failed, index, type='radio') => {
    const check_type = document.querySelector('#one_list');
    if (check_type.checked) {
        type = 'radio';
        name = 'right_answer'
    } else {
        type = 'checkbox';
        name = `right_answer/${index}`;
    }
    let answer_feild__ = `<div class="input-group answer_element_${index}">
         <div class="input-group-text">
                <input class="form__radio_btn" type="${type}" name="${name}" value="${index}" checked>
         </div>
         <input type="text" class="form-control" name="answer/${index}" value="${answer_failed}" required>
         <div class="btn btn__minus" id="btn__minus"><img src="/static/src/minus.png"></div>
         </div>`;
    return answer_feild__;
};

const paint_container_answers = () => {
    const container_answers = list_answers.map((answer_failed, index) => get_answer_failed(answer_failed, index)).join("");
    return container_answers;
};

const refresh_container_answers = () => {
    removeAllChildNodes(cont_answersNode);
    cont_answersNode.insertAdjacentHTML('beforeend', paint_container_answers());
    refresh_listen_minus();
}

const refresh_container_answers_plus = () => {
    removeAllChildNodes(cont_answersNode);
    cont_answersNode.insertAdjacentHTML('beforeend', paint_container_answers());
}

const refresh_listen_minus = () => {
    const minusNode = document.querySelectorAll('#btn__minus')
    for (let i = 0; i < minusNode.length; i++){
        let minus = minusNode[i];
        minus.addEventListener("click", function() {refresh_list_answer_value(); list_answers.splice(i,1); console.log(i); refresh_container_answers()});
    }
}

const refresh_list_answer_value = () => {
    list_answers = []
    const answers_values = document.querySelectorAll(".form-control")
    for (let answer_values of answers_values){
        list_answers.push(answer_values.value)
    }
    console.log(list_answers)
}

const insert_answers = () => {
    refresh_list_answer_value()
    list_answers.push('');

    refresh_container_answers_plus()

    const minusNode = document.querySelectorAll('#btn__minus')

    refresh_listen_minus()
};


insert_answers()

plusNode.addEventListener("click", insert_answers);


const hiden_group_add = () => {
    groupNode.classList.add("hidden");
    groupAnswers.classList.add("hidden");
    oneAnswer.classList.remove("hidden");


}

const hiden_group_del = () => {
    groupNode.classList.remove("hidden");
    groupAnswers.classList.remove("hidden");
    oneAnswer.classList.add("hidden");

}


isOpenNode.addEventListener("click", hiden_group_add)
isClosedNode.addEventListener("click", hiden_group_del)


const refresh_container_answers_check = () => {
    refresh_list_answer_value();
    removeAllChildNodes(cont_answersNode);
    cont_answersNode.insertAdjacentHTML('beforeend', list_answers.map((answer_failed, index) => get_answer_failed(answer_failed, index, type='checkbox')).join(""));
    refresh_listen_minus();
}

const refresh_container_answers_radio = () => {
    refresh_list_answer_value();
    removeAllChildNodes(cont_answersNode);
    cont_answersNode.insertAdjacentHTML('beforeend', list_answers.map((answer_failed, index) => get_answer_failed(answer_failed, index, type='radio')).join(""));
    refresh_listen_minus();
};

isAnylistNode.addEventListener("click", refresh_container_answers_check);
isOnelistNode.addEventListener("click", refresh_container_answers_radio);


const dell_answers_grup = () => {
    if (isOpenNode.checked) {
        groupAnswers.remove();
        groupNode.remove();
    } else {
        oneAnswerNode.remove();
    }
};


subBtnNode = document.querySelector('.sub')
subBtnNode.addEventListener("click", dell_answers_grup);





