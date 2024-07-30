document.addEventListener('DOMContentLoaded', function() {
    var addImageFormButton = document.getElementById('add-image-form');
    var imageFormSet = document.getElementById('image_formset');
    var totalForms = document.getElementById('id_form-TOTAL_FORMS');
    var formIndex = imageFormSet.childElementCount;

    addImageFormButton.addEventListener('click', function() {
        var newForm = imageFormSet.children[0].cloneNode(true);
        var formRegex = new RegExp(`form-(\\d){1}-`, 'g');
        formIndex++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formIndex}-`);
        var newFormDeleteInput = newForm.querySelector('input[type="checkbox"]');
        if (newFormDeleteInput) {
            newFormDeleteInput.checked = false;
        }
        imageFormSet.appendChild(newForm);
        totalForms.setAttribute('value', formIndex + 1);
    });
});