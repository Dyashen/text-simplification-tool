  /* --- */
  const checkbox = document.querySelector('#personalizedSummary');
  const fieldsets = document.querySelectorAll('.personalized');
  checkbox.addEventListener('change', () => {
    fieldsets.forEach(fieldset => {
      if (checkbox && checkbox.checked) {
        fieldset.style.display = 'block';
      } else {
        fieldset.style.display = 'none';
      }
    });
  });

  /* Add word to glossary */
  var checkboxAddWordToGlossary = document.getElementById("checkboxAddWordToGlossary");
  checkboxAddWordToGlossary.addEventListener("change", function () {
    if (checkboxAddWordToGlossary && checkboxAddWordToGlossary.checked) {
      const words = document.querySelectorAll("span.verb, span.noun, span.aux, span.verb, span.adj");
      words.forEach((w) => {
        w.addEventListener('click', async (event) => {
          if (checkboxAddWordToGlossary.checked) {
            var pTag = event.target;
            sentence_of_origin = w.closest("span.sentence");
            var context = "";
            for (const child of sentence_of_origin.children) { context = context + " " + child.textContent };
            console.log(context);
            var textarea = document.getElementById("glossaryList");
            pTag.style.backgroundColor = "black";
            pTag.style.color = "white";
            pTag.style.fontWeight = "bold";
            textarea.value += pTag.innerHTML + ':' + context + "\n";
            console.log(textarea.value);
          }
        })
      })
    }
  });

  /* Deleting sentences */
  const checkboxDeleteSents = document.getElementById("checkboxDeleteSents");
  checkboxDeleteSents.addEventListener("change", function () {
    if (checkboxDeleteSents && checkboxDeleteSents.checked) {
      const sentences = document.querySelectorAll('.sentence');
      sentences.forEach((span) => {
        span.addEventListener('click', async (event) => {
          if (checkboxDeleteSents.checked) span.remove();
        })
      })
    }
  });

  /* Tekst toevoegen */
  function addTextToTextArea() {
    const fullTextBox = document.querySelector('.left-container').innerHTML
    var textarea = document.getElementById("fullText");
    textarea.value = fullTextBox;
    document.getElementById('summarize-with-presets-button').disabled = false;
  };

  /* Tekst ophalen */
  async function getSelectedText() {
    var selectedText = window.getSelection().toString();
    const textarea = document.querySelector('textarea');
    textarea.value = selectedText;
  };