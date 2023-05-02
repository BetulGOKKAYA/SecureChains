const url = window.location.href
const riskEditBox = document.getElementById('risk-edit-box')
const modalBody = document.getElementById('modal-body-confirm')
const updateBtn = document.getElementById('start-button')
 
$.ajax({
    type: 'GET',
    url: `${url}edit/`,
    success: function (response) {
        const data = response.data;

        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                const _answer = answers['answer'];
                const user_answer = answers['user_answer'];

                riskEditBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        ${question}
                    </div>
                    <div class="mb-2">
                        <b>Your answer for this question was " ${user_answer} " </b>
                    </div>
                `;

                _answer.forEach(answer => {
                    riskEditBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}-${answer}">${answer}</label>
                        </div>
                    `;
                });
            }
        });

        // Add event listeners to radio buttons
        const radioButtons = document.querySelectorAll('.ans');
        radioButtons.forEach(radioButton => {
            radioButton.addEventListener('click', function () {
                if (this.dataset.checked) {
                    this.checked = false;
                    delete this.dataset.checked;
                } else {
                    this.dataset.checked = "true";
                }
            });
        });
    },
    error: function (error) {
        console.log(error);
    },
});

const riskForm = document.getElementById('risk-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {
        
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if(el.checked){
            data[el.name]=el.value

        }else{
            if(!data[el.name]){
                data[el.name] = null
            }
        }
        
    })
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){

            

             
            
        },
        error: function(error){
            console.log(error)
        }
    })



}



riskForm.addEventListener('submit', e=>{
    e.preventDefault()

    modalBody.innerHTML = `
    <div class="h5 mb-3">Are you sure you want to update your responses ?</div>
    <div class="text-muted">

    </div>
`

updateBtn.addEventListener('click', ()=>{
    sendData()
    location.reload();
})

    
})

 
 