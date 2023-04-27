/* --- Toggle Text Input --- */
document.getElementById('toggleFullTextScholars').addEventListener('change', function () {
    if (this.checked) {
      var textarea = document.createElement('textarea');
      textarea.name = 'fullText';
      this.form.appendChild(textarea);
    } else {
      var textarea = this.form.querySelector('textarea[name="fullText"]');
      if (textarea) {
        textarea.remove();
      }
    }
  });


  document.getElementById('toggleFullTextTeachers').addEventListener('change', function () {
    if (this.checked) {
      var textarea = document.createElement('textarea');
      textarea.name = 'fullText';
      this.form.appendChild(textarea);
    } else {
      var textarea = this.form.querySelector('textarea[name="fullText"]');
      if (textarea) {
        textarea.remove();
      }
    }
  });