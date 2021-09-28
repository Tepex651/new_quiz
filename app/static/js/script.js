count = 1

function createDiv() {
  var btn = document.getElementById('buttons');
  btn.insertAdjacentHTML("beforeBegin", '<div id="new_row" class="field has-addons" style="margin: 0; margin-bottom: 0.5rem; height: 40px;">\
                                          <p class="control is-expanded">\
                                            <input class="input" type="text" name="new_answer_name" required>\
                                          </p>\
                                          <p class="control" style="">\
                                            <label class="checkbox" style="height: 100%;">\
                                              <input id="checkbox-value" type="hidden" name="new_answer_correct" value="False">\
                                              <input id="checkbox" type="checkbox" style="width: 40px; height: 40px;" onClick="stateCheckbox(this)">\
                                            </label>\
                                          </p>\
                                          <p class="control">\
                                            <a class="delete is-medium mx-2" aria-label="delete" style="top: 50%; margin-top: -12px;" onClick="deleteDiv(this)"></a>\
                                          </p>\
                                        </div>');
  }

function deleteDiv(elem) {
    var mainDiv = elem.parentNode.parentNode;
    mainDiv.remove();
};

function stateCheckbox(elem) {
  var parent = elem.parentNode;
  var hiddenbox = parent.firstElementChild;
  if (elem.checked) {
    hiddenbox.value='True';
  } else {
    hiddenbox.value='False';
  }
}


function closeModal(elem) {
  var mainModal = elem.parentNode.parentNode.parentNode;
  mainModal.remove();
}