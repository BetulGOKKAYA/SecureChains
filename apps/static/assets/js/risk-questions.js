// Define variables to access DOM elements
const url = window.location.href
const _url = window.location.href
const riskBox = document.getElementById('risk-box')
const saveBox = document.getElementById('save-box')
const saveBtn = document.getElementById('submit-btn');
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
const modalBtns =document.getElementsByClassName('modal-button')
const infoBtn = document.getElementById('btn-info')
const infoText = "Information about the question";
const div = document.createElement('div');

 
  
// Make a GET request to the server to fetch question data from view.py 
$.ajax({
    type: 'GET',
    url: `${url}data/`,
    success: function(response){
      // Extract data and metadata from the response
        const data = response.data
        const metadata = response.metadata

        // Loop through each question and its answers
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
 
                 // Add question to the DOM
                riskBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `

            // Loop through metadata to find additional information for each question
              metadata.forEach(meta => {
                for (const [key, value] of Object.entries(meta)) {
                    if(key==question){
                      // Add info button to the DOM
                        riskBox.innerHTML += `
                        <div class="mb-2"> 
                        <button type="button" class="info-button" id="${value}" ><b>i</b></button>
                        </div>
                        `
                    }
        
 
                }
            });
            // Loop through answers and add them to the DOM
            answers.forEach(answer=>{
                riskBox.innerHTML += `
                    <div>
                        <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                        <label for="${question}">${answer}</label>
                       
                    </div>
                `
            })
                


            }
        });

        
       // Attach event listeners to info buttons for displaying additional information
        const infoButton = document.querySelectorAll('.info-button');
        infoButton.forEach(button => { 
            button.addEventListener('click', () => {
                const id = button.id;
                const metadata = response.metadata; 
 
 
                let info;
                // Find the corresponding info for the clicked button
                for (const [key, value] of Object.entries(metadata)) {
 
                    if(key==id)
                    console.log("oldu dadsa");
                    else
                    info = id

                  } 

                  alert(`${info}`);
              });
          });
 
        
    },
    error: function(error){
        console.log(error)
    }
})

 


const riskForm = document.getElementById('risk-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


// Function to check if all questions have been answered
// Function to check if all questions have been answered
const allQuestionsAnswered = (elements) => {
  const answeredQuestions = new Set();
  const totalQuestions = new Set();

  elements.forEach((el) => {
    totalQuestions.add(el.name);
    if (el.checked) {
      answeredQuestions.add(el.name);
    }
  });

  return answeredQuestions.size === totalQuestions.size;
};


 
// Function to send form data to the server
const sendData = () => {
    const elements = [...document.getElementsByClassName("ans")];
    const data = {};
    data["csrfmiddlewaretoken"] = csrf[0].value;

    
    
    elements.forEach((el) => {
      if (el.checked) {
        data[el.name] = el.value;
      } else {
        if (!data[el.name]) {
          data[el.name] = null;
        }
      }
    });
  
    if (!allQuestionsAnswered(elements)) {
      alert("Please answer all questions before submitting.");
      return;
    }
  
    // Send form data to the server
    $.ajax({
      type: "POST",
      url: `${url}save/`,
      data: data,
      success: function(response){
        _url: `${url}data/`

        window.location.replace(_url)    
      },
      error: function (error) {
        console.log(error);
      },
    });
  };
  



// Attach event listeners to the form
riskForm.addEventListener("submit", (e) => {
  e.preventDefault();

  modalBody.innerHTML = `
    <div class="h5 mb-3">Are you sure you want to submit your responses ?</div>
    <div class="text-muted">
    </div>
  `;
});

startBtn.addEventListener("click", () => {
  const elements = [...document.getElementsByClassName("ans")];

  if (riskBox.childElementCount === 0) {
    alert("There are no questions. Please go back to the dashboard.");
    return;
  }

  if (!allQuestionsAnswered(elements)) {
    alert("Please answer all questions before submitting.");
    return;
  } else {
    sendData();
  }
});
