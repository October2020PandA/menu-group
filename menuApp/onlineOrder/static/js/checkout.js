// var pickUp = document.getElementById('pickup')
// pickUp.addEventListener('click', function(){
//     document.getElementById('delivery-order').classList.add("invisible");
// })

// var delivery = document.getElementById('delivery')
// delivery.addEventListener('click', function(){
//     document.getElementById('delivery-order').classList.remove("invisible");
// })

var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.product
        var action = this.dataset.action
        console.log('itemtId:', itemId, 'action:', action)
    })
}

function updateUserOrder(itemId, action){
    
    var url = '/update_item'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'itemId':itemId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}

