var pickUp = document.getElementById('pickup')
pickUp.addEventListener('click', function(){
    document.getElementById('delivery-order').classList.add("invisible");
})

var delivery = document.getElementById('delivery')
delivery.addEventListener('click', function(){
    document.getElementById('delivery-order').classList.remove("invisible");
})

