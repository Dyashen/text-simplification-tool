  /* --- */
  const checkbox = document.querySelector('#personalizedSummary');
  const fieldsets = document.querySelectorAll('.personalized');
  checkbox.addEventListener('change', () => {
    fieldsets.forEach(fieldset => {
      if (checkbox.checked) {
        fieldset.style.display = 'block';
      } else {
        fieldset.style.display = 'none';
      }
    });
  });

  /* Glossary-lijst aanvullen met woord */
  const checkboxAddWordToGlossary = document.getElementById("checkboxAddWordToGlossary");
  checkboxAddWordToGlossary.addEventListener("change", function () {
    if (checkboxAddWordToGlossary.checked) {
      const words = document.querySelectorAll('span.noun', 'span.aux', 'span.verb', 'span.adj');
      words.forEach((w) => {
        w.addEventListener('click', async (event) => {
          if (checkboxAddWordToGlossary.checked) {
            var pTag = event.target;
            sentence_of_origin = w.closest("span.sentence");
            var context = "";
            for (const child of sentence_of_origin.children) { context = context + " " + child.textContent };
            const response = await fetch(`http://localhost:5000/get-pos-tag?word=${w.textContent}&context=${context}`);
            result = await response.json();
            var pos_tag = JSON.stringify(result.pos);

            var textarea = document.getElementById("glossaryList");
            pTag.style.backgroundColor = "black";
            pTag.style.color = "white";
            pTag.style.fontWeight = "bold";
            var page = pTag.parentNode.parentNode.parentNode;
            var pageNumber = page.querySelector('h1').textContent;
            textarea.value += pTag.innerHTML + ':' + pageNumber + ':' + pos_tag + "\n";
          }
        })
      })
    }
  });

  /* Deleting sentences */
  const checkboxDeleteSents = document.getElementById("checkboxDeleteSents");
  checkboxDeleteSents.addEventListener("change", function () {
    if (checkboxDeleteSents.checked) {
      const sentences = document.querySelectorAll('.sentence');
      sentences.forEach((span) => {
        span.addEventListener('click', async (event) => {
          if (checkboxDeleteSents.checked) span.remove();
        })
      })
    }
  });


  /* Marking titles as a teacher */
  const checkboxTitle = document.getElementById("checkboxTitle");
  checkboxTitle.addEventListener("change", function () {
    if (checkboxTitle.checked) {
      const sentences = document.querySelectorAll('.sentence');
      sentences.forEach((span) => {
        span.addEventListener('click', async (event) => {
          if (checkboxTitle.checked) {
            var title = document.createElement("h3");
            title.innerHTML = span.innerHTML;
            span.parentNode.replaceChild(title, span);
          };
        });
      });
    }
  });


  /* Tekst toevoegen */
  function addTextToTextArea() {
    console.log(document.querySelector('.left-container').innerHTML);
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