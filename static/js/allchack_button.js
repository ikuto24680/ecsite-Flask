/**
 * 
 */
  const checkbox = document.getElementsByName("toppingList")

  function checkAllBox(trueOrFalse) {
  for(i = 0; i < checkbox.length; i++) {
   checkbox[i].checked = trueOrFalse
  }
   }